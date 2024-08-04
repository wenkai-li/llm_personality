from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os


class LLAMA3():
    def __init__(self, llama_version, model_id, cache_dir=None, mode='direct'):
        """
        mode:
        - 'direct': direct inference of llama3
        - 'prompt_xxxxx': set the personality traits by prompting
        """
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            cache_dir=cache_dir
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            cache_dir=cache_dir
        )

        self.terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        self.mode = mode
    
    def generate(self, prompts, **gen_kwargs):
        if self.mode == 'direct':
            messages = [
                {"role": "user", "content": prompts}
            ]
        else:
            raise NotImplementedError

        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)

        # outputs = self.model.generate(
        #     input_ids,
        #     max_new_tokens=256,
        #     eos_token_id=self.terminators,
        #     do_sample=True,
        #     temperature=0.6,
        #     top_p=0.9,
        # )
        outputs = self.model.generate(
            input_ids,
            eos_token_id=self.terminators,
            **gen_kwargs,
        )
        
        response = outputs[0][input_ids.shape[-1]:]
        result = self.tokenizer.decode(response, skip_special_tokens=True)
        return result