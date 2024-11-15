#!/bin/bash
MODEL_NAME_OR_PATH="/data/user_data/wenkail/.cache/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/e1945c40cd546c78e41f1151f4db032b271faeaa"
OUTPUT_DIR="/data/user_data/wenkail/llm_personality/llama_big_five_epoch1"
# CHAT_FORMAT_PATH="/home/wenkail/AMEFT/LLaMA-Factory/llama3.jinja"
export HF_TOKEN="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"
source ~/.bashrc
conda activate llama_factory
deepspeed --master_port 29501 --num_gpus 4 \
    src/train_bash.py \
    --deepspeed examples/deepspeed/ds_z3_config.json \
    --stage sft \
    --do_train \
    --model_name_or_path=$MODEL_NAME_OR_PATH \
    --dataset alpaca_big_five_dataset_train \
    --dataset_dir ./data \
    --template llama3 \
    --finetuning_type full \
    --output_dir=$OUTPUT_DIR \
    --overwrite_cache \
    --overwrite_output_dir \
    --cutoff_len 2048 \
    --preprocessing_num_workers 16 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --warmup_steps 20 \
    --save_steps 1000 \
    --eval_steps 1000 \
    --evaluation_strategy steps \
    --load_best_model_at_end \
    --learning_rate 5e-4 \
    --num_train_epochs 1 \    # --num_train_epochs 40 \     # --max_samples 1000 \
    --val_size 0.1 \
    --plot_loss \
    --fp16 \
    --report_to 'wandb'
