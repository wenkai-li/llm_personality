# Copyright 2024 HuggingFace Inc. and the LlamaFactory team.
#
# This code is inspired by the HuggingFace's TRL library.
# https://github.com/huggingface/trl/blob/v0.8.0/trl/trainer/dpo_trainer.py
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import warnings
from collections import defaultdict
from contextlib import nullcontext
from types import MethodType
from typing import TYPE_CHECKING, Dict, Literal, Optional, Tuple, Union

import torch
import torch.nn.functional as F
from transformers import Trainer
from trl import DPOTrainer
from trl.trainer import disable_dropout_in_model
import pdb
from ...extras.constants import IGNORE_INDEX
from ..trainer_utils import convert_pissa_adapter, create_custom_optimzer, create_custom_scheduler, get_batch_logps


if TYPE_CHECKING:
    from transformers import PreTrainedModel, ProcessorMixin

    from ...hparams import FinetuningArguments


class CustomDPOTrainer(DPOTrainer):
    def __init__(
        self,
        model: Union["PreTrainedModel", torch.nn.Module],
        ref_model: Optional[Union["PreTrainedModel", torch.nn.Module]],
        finetuning_args: "FinetuningArguments",
        processor: Optional["ProcessorMixin"],
        disable_dropout: bool = True,
        **kwargs,
    ):
        if disable_dropout:
            disable_dropout_in_model(model)
            if ref_model is not None:
                disable_dropout_in_model(ref_model)

        self.finetuning_args = finetuning_args
        self.processor = processor
        self.reference_free = False
        self.use_dpo_data_collator = True  # hack to avoid warning
        self.generate_during_eval = False  # disable at evaluation
        self.label_pad_token_id = IGNORE_INDEX
        self.padding_value = 0
        self.is_encoder_decoder = model.config.is_encoder_decoder
        self.precompute_ref_log_probs = False
        self._precomputed_train_ref_log_probs = False
        self._precomputed_eval_ref_log_probs = False
        self._peft_has_been_casted_to_bf16 = False

        self.ref_model = ref_model
        self._stored_metrics = defaultdict(lambda: defaultdict(list))

        # dpo hyperparams
        self.beta = finetuning_args.pref_beta
        self.loss_type = finetuning_args.pref_loss
        self.ftx_gamma = finetuning_args.pref_ftx
        self.label_smoothing = finetuning_args.dpo_label_smoothing
        self.simpo_gamma = finetuning_args.simpo_gamma

        Trainer.__init__(self, model=model, **kwargs)
        if not hasattr(self, "accelerator"):
            raise AttributeError("Please update `transformers`.")

        warnings.simplefilter("ignore")  # remove gc warnings on ref model

        if ref_model is not None:
            if self.is_deepspeed_enabled:
                if not (
                    getattr(ref_model, "is_loaded_in_8bit", False) or getattr(ref_model, "is_loaded_in_4bit", False)
                ):  # quantized models are already set on the correct device
                    self.ref_model = self._prepare_deepspeed(self.ref_model)
            else:
                self.ref_model = self.accelerator.prepare_model(self.ref_model, evaluation_mode=True)
                self.ref_model.eval()

        if finetuning_args.pissa_convert:
            self.save_model(os.path.join(self.args.output_dir, "pissa_init"))

        if finetuning_args.use_badam:
            from badam import BAdamCallback, clip_grad_norm_old_version

            self.accelerator.clip_grad_norm_ = MethodType(clip_grad_norm_old_version, self.accelerator)
            self.callback_handler.add_callback(BAdamCallback)

    def create_optimizer(self) -> "torch.optim.Optimizer":
        if self.optimizer is None:
            self.optimizer = create_custom_optimzer(self.model, self.args, self.finetuning_args)
        return super().create_optimizer()

    def create_scheduler(
        self, num_training_steps: int, optimizer: Optional["torch.optim.Optimizer"] = None
    ) -> "torch.optim.lr_scheduler.LRScheduler":
        create_custom_scheduler(self.args, num_training_steps, optimizer)
        return super().create_scheduler(num_training_steps, optimizer)

    def _save(self, output_dir: Optional[str] = None, state_dict: Optional[Dict[str, "torch.Tensor"]] = None) -> None:
        super()._save(output_dir, state_dict)
        output_dir = output_dir if output_dir is not None else self.args.output_dir
        if self.finetuning_args.pissa_convert:
            convert_pissa_adapter(output_dir, state_dict, self.accelerator, self.model, self.args)

        if self.processor is not None:
            getattr(self.processor, "image_processor").save_pretrained(output_dir)

    def odds_ratio_loss(self, chosen_logps: "torch.Tensor", rejected_logps: "torch.Tensor") -> "torch.Tensor":
        r"""
        Computes ORPO's odds ratio (OR) loss for batched log probabilities of the policy model.
        """
        log_odds = (chosen_logps - rejected_logps) - (
            torch.log1p(-torch.exp(chosen_logps)) - torch.log1p(-torch.exp(rejected_logps))
        )
        sft_loss = -chosen_logps
        odds_ratio_loss = -F.logsigmoid(log_odds)
        orpo_loss = sft_loss + self.beta * odds_ratio_loss
        return orpo_loss
    
    def triple_loss(self, chosen_logps: "torch.Tensor", rejected_logps_1: "torch.Tensor", rejected_logps_2: "torch.Tensor") -> "torch.Tensor":
        exp_chosen = torch.exp(chosen_logps)
        exp_rejected = torch.exp(rejected_logps_1)
        exp_rejected_reject = torch.exp(rejected_logps_2)
        sum_exp = exp_chosen + exp_rejected + exp_rejected_reject
        cross_entropy_loss = -torch.log(exp_chosen / sum_exp)
        
        # log_odds_1 = (chosen_logps - rejected_logps_1) - (
        #     torch.log1p(-torch.exp(chosen_logps)) - torch.log1p(-torch.exp(rejected_logps_1))
        # )
        # log_odds_2 = (chosen_logps - rejected_logps_2) - (
        #     torch.log1p(-torch.exp(chosen_logps)) - torch.log1p(-torch.exp(rejected_logps_2))
        # )
        # odds_ratio_loss_1 = -F.logsigmoid(log_odds_1)
        # odds_ratio_loss_2 = -F.logsigmoid(log_odds_2)
        triple_loss = cross_entropy_loss
        return triple_loss
        
    def simpo_loss(self, chosen_logps: "torch.Tensor", rejected_logps: "torch.Tensor") -> "torch.Tensor":
        r"""
        Computes SimPO loss for batched log probabilities of the policy model.
        """
        pi_logratios = chosen_logps - rejected_logps
        gamma_logratios = self.simpo_gamma / self.beta
        logits = pi_logratios - gamma_logratios
        simpo_loss = -F.logsigmoid(self.beta * logits)
        return simpo_loss

    # TODO: Add the third rejected logps
    def compute_preference_loss(
        self,
        policy_chosen_logps: "torch.Tensor",
        policy_rejected_logps_1: "torch.Tensor",
        policy_rejected_logps_2: "torch.Tensor",
        reference_chosen_logps: Optional["torch.Tensor"],
        reference_rejected_logps_1: Optional["torch.Tensor"],
        reference_rejected_logps_2: Optional["torch.Tensor"],
    ) -> Tuple["torch.Tensor", "torch.Tensor", "torch.Tensor"]:
        r"""
        Computes loss for preference learning.
        """
        
        if not self.finetuning_args.use_ref_model:
            # if self.loss_type == "orpo":
            #     losses = self.odds_ratio_loss(policy_chosen_logps, policy_rejected_logps)
            # elif self.loss_type == "simpo":
            #     losses = self.simpo_loss(policy_chosen_logps, policy_rejected_logps)
            # el
            if self.loss_type == "triple":
                losses = self.triple_loss(policy_chosen_logps, reference_rejected_logps_1, reference_rejected_logps_2)
            else:
                raise NotImplementedError("Unknown loss type: {}.".format(self.loss_type))
            
            # if self.loss_type in ['orpo', 'simpo']:
            #     chosen_rewards = self.beta * policy_chosen_logps.to(self.accelerator.device).detach()
            #     rejected_rewards = self.beta * policy_rejected_logps.to(self.accelerator.device).detach()
            # el
            if self.loss_type in ['triple']:
                chosen_rewards = self.beta * policy_chosen_logps.to(self.accelerator.device).detach()
                rejected_rewards_1 = self.beta * policy_rejected_logps_1.to(self.accelerator.device).detach()
                rejected_rewards_2 = self.beta * policy_rejected_logps_2.to(self.accelerator.device).detach()
            
        return losses, chosen_rewards, rejected_rewards_1, rejected_rewards_2
        # else:
        #     losses, chosen_rewards, rejected_rewards = self.dpo_loss(
        #         policy_chosen_logps, policy_rejected_logps, reference_chosen_logps, reference_rejected_logps
        #     )

        # return losses, chosen_rewards, rejected_rewards

    def concatenated_forward(
        self, model: "PreTrainedModel", batch: Dict[str, "torch.Tensor"]
    ) -> Tuple["torch.Tensor", "torch.Tensor", "torch.Tensor", "torch.Tensor", "torch.Tensor"]:
        r"""
        Computes the sum log probabilities of the labels under given logits if loss_type is not IPO, ORPO or SimPO.

        Otherwise the average log probabilities.
        """
        if self.finetuning_args.use_ref_model:
            batch = {k: v.detach().clone() for k, v in batch.items()}  # avoid error

        all_logits: "torch.Tensor" = model(**batch, return_dict=True, use_cache=False).logits.to(torch.float32)

        all_logps, valid_length = get_batch_logps(logits=all_logits, labels=batch["labels"])
        if self.loss_type in ["ipo", "orpo", "simpo", "triple"]:
            all_logps = all_logps / valid_length
        if self.loss_type in ["ipo", "orpo", "simpo"]:
            batch_size = batch["input_ids"].size(0) // 2
            chosen_logps, rejected_logps = all_logps.split(batch_size, dim=0)
            chosen_logits, rejected_logits = all_logits.split(batch_size, dim=0)
            chosen_length, _ = valid_length.split(batch_size, dim=0)
            return chosen_logps, rejected_logps, chosen_logits, rejected_logits, chosen_logps / chosen_length
        elif self.loss_type == "triple":
            # print(f"Batch Size: { batch['input_ids'].size()}")
            batch_size = batch["input_ids"].size(0) // 3
            # pdb.set_trace()
            chosen_logps, rejected_logps_1, rejected_logps_2 = all_logps.split(batch_size, dim=0)
            chosen_logits, rejected_logits_1, rejected_logits_2 = all_logits.split(batch_size, dim=0)
            chosen_length, _, _ = valid_length.split(batch_size, dim=0)
            return chosen_logps, rejected_logps_1, rejected_logps_2, chosen_logits, rejected_logits_1, rejected_logits_2, chosen_logps / chosen_length

    # Customize Compute Loss
    def compute_loss(self, model: "PreTrainedModel", inputs, return_outputs=False):
        """
        How the loss is computed by Trainer. By default, all models return the loss in the first element.

        Subclass and override for custom behavior.
        """
        
        if self.label_smoother is not None and "labels" in inputs:
            labels = inputs.pop("labels")
        else:
            labels = None
        outputs = model(**inputs)
        # Save past state if it exists
        # TODO: this needs to be fixed and made cleaner later.
        if self.args.past_index >= 0:
            self._past = outputs[self.args.past_index]

        if labels is not None:
            unwrapped_model = self.accelerator.unwrap_model(model)
            if _is_peft_model(unwrapped_model):
                model_name = unwrapped_model.base_model.model._get_name()
            else:
                model_name = unwrapped_model._get_name()
            if model_name in MODEL_FOR_CAUSAL_LM_MAPPING_NAMES.values():
                loss = self.label_smoother(outputs, labels, shift_labels=True)
            else:
                loss = self.label_smoother(outputs, labels)
        else:
            if isinstance(outputs, dict) and "loss" not in outputs:
                raise ValueError(
                    "The model did not return a loss from the inputs, only the following keys: "
                    f"{','.join(outputs.keys())}. For reference, the inputs it received are {','.join(inputs.keys())}."
                )
            # We don't use .loss here since the model may return tuples instead of ModelOutput.
            loss = outputs["loss"] if isinstance(outputs, dict) else outputs[0]
        # print(f"Outputs: {outputs}")
        return (loss, outputs) if return_outputs else loss

    def compute_reference_log_probs(
        self, model: "PreTrainedModel", batch: Dict[str, "torch.Tensor"]
    ) -> Tuple[Optional["torch.Tensor"], Optional["torch.Tensor"]]:
        r"""
        Computes log probabilities of the reference model.
        """
        if not self.finetuning_args.use_ref_model:
            return None, None

        if self.ref_model is None:
            ref_model = model
            ref_context = self.accelerator.unwrap_model(model).disable_adapter()
        else:
            ref_model = self.ref_model
            ref_context = nullcontext()

        with torch.no_grad(), ref_context:
            reference_chosen_logps, reference_rejected_logps, *_ = self.concatenated_forward(ref_model, batch)

        return reference_chosen_logps, reference_rejected_logps

    def get_batch_loss_metrics(
        self,
        model: "PreTrainedModel",
        batch: Dict[str, "torch.Tensor"],
        train_eval: Literal["train", "eval"] = "train",
    ) -> Tuple["torch.Tensor", Dict[str, "torch.Tensor"]]:
        r"""
        Computes the DPO loss and other metrics for the given batch of inputs for train or test.
        """
        metrics = {}
        (
            policy_chosen_logps,
            policy_rejected_logps_1,
            policy_rejected_logps_2,
            policy_chosen_logits,
            policy_rejected_logits_1,
            policy_rejected_logits_2,
            policy_chosen_logps_avg,
        ) = self.concatenated_forward(model, batch)

        reference_chosen_logps, reference_rejected_logps_1, reference_rejected_logps_2 = self.compute_reference_log_probs(model, batch)
        losses, chosen_rewards, rejected_rewards_1, rejected_rewards_2 = self.compute_preference_loss(
            policy_chosen_logps,
            policy_rejected_logps_1,
            policy_rejected_logps_2,
            reference_chosen_logps,
            reference_rejected_logps_1,
            reference_rejected_logps_2,
        )
        
        # sft_loss = -policy_chosen_logps_avg
        # if self.ftx_gamma > 1e-6:
        #     losses += self.ftx_gamma * sft_loss

        # reward_accuracies = (chosen_rewards > rejected_rewards).float()
        reward_accuracies_1 = (chosen_rewards > rejected_rewards_1).float()
        reward_accuracies_2 = (chosen_rewards > rejected_rewards_2).float()

        prefix = "eval_" if train_eval == "eval" else ""
        metrics["{}rewards/chosen".format(prefix)] = chosen_rewards.mean().cpu()
        metrics["{}rewards/rejected_1".format(prefix)] = rejected_rewards_1.mean().cpu()
        metrics["{}rewards/rejected_2".format(prefix)] = rejected_rewards_2.mean().cpu()
        metrics["{}rewards/accuracies_1".format(prefix)] = reward_accuracies_1.mean().cpu()
        metrics["{}rewards/accuracies_2".format(prefix)] = reward_accuracies_2.mean().cpu()
        metrics["{}rewards/margins_1".format(prefix)] = (chosen_rewards - rejected_rewards_1).mean().cpu()
        metrics["{}rewards/margins_2".format(prefix)] = (chosen_rewards - rejected_rewards_2).mean().cpu()
        metrics["{}logps/rejected_1".format(prefix)] = policy_rejected_logps_1.detach().mean().cpu()
        metrics["{}logps/rejected_2".format(prefix)] = policy_rejected_logps_2.detach().mean().cpu()
        metrics["{}logps/chosen".format(prefix)] = policy_chosen_logps.detach().mean().cpu()
        metrics["{}logits/rejected_1".format(prefix)] = policy_rejected_logits_1.detach().mean().cpu()
        metrics["{}logits/rejected_2".format(prefix)] = policy_rejected_logits_2.detach().mean().cpu()
        metrics["{}logits/chosen".format(prefix)] = policy_chosen_logits.detach().mean().cpu()

        return losses.mean(), metrics

