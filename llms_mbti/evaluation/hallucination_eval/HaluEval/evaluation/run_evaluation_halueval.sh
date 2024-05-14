#!/bin/bash

MODEL_PATH="/data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/full_finetune/thinking/checkpoint-350"

source ~/.bashrc
conda activate llm_personality

cd ~/llm_personality/llms_mbti/evaluation/hallucination_eval/HaluEval/evaluation
python evaluate_with_vllm.py --task qa --model llama_13b_thinking_fullfinetune --model_path=$MODEL_PATH 

# --lora False --lora_type dpo --lora_path /data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/lora/thinking/checkpoint-12000

# --lora True --lora_type dpo --lora_path /data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/lora/enfp/checkpoint-15000