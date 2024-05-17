#!/bin/bash

# parameters
MATHOD="zero_shot"
MODEL="llama-13b"
MODEL_PATH="/data/models/huggingface/meta-llama/Llama-2-13b-chat-hf"
LORA_PATH="/data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/lora/istj/checkpoint-12000"
DATASET="gsm8k"


source ~/.bashrc
conda activate llm_personality
cd ~/llm_personality/llms_mbti/evaluation/math_eval/grade-school-math/grade_school_math
python evaluate.py --method=$MATHOD --model=$MODEL --dataset=$DATASET --model_path=$MODEL_PATH --limit_dataset_size 5
#  --use_lora True --lora_path $LORA_PATH


# LLaMa-13b-unfinetuned
# with zero-shot:
# The accuracy is 6.1410159211523885%

# LLaMa-13b-unfinetuned
# with zero-shot-cot:
# The accuracy is 28.582259287338896%

# LLaMa-13b-dpo-finetuned-checkpoint-12000-istj
# with zero-shot:
# The accuracy is 3.56330553449583%

# LLaMa-13b-dpo-finetuned-checkpoint-12000-istj
# with zero-shot-cot:
# The accuracy is 14.935557240333585

# LLaMa-13b-dpo-finetuned-checkpoint-12000-enfp
# with zero-shot:
# The accuracy is 

# LLaMa-13b-dpo-finetuned-checkpoint-12000-thinking
# with zero-shot:
# The accuracy is 