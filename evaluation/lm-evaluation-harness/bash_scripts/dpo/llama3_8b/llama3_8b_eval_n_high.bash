# set -e

# Remember to change the results path, please put it in the results folder
BASE_DIRECTORY="/home/wenkail/llm_personality/evaluation/lm-evaluation-harness/results/dpo/llama3_8b_n_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
SYSTEM_PROMPT="You are a helpful assistant with the following Big Five personality traits: Neuroticism - high"
BATCH_SIZE=16
MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"

source ~/.bashrc

echo "Activating lm_eval environment..."
conda activate lm_eval

# Social reasoning benchmark
echo "Do the Llama 3 8B SocialIQA Evaluation"
TASK_NAME="social_iqa"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# General Benchmark
# General:
echo "Do the Llama 3 8B MMLU Evaluation"
TASK_NAME="mmlu"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# Commonsing Reasoning
echo "Do the Llama 3 8B PIQA Evaluation"
TASK_NAME="piqa"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B CommonsenseQa Evaluation"
TASK_NAME="commonsense_qa"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B GPQA Main Zero Shot Evaluation"
TASK_NAME="gpqa_main_zeroshot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B GPQA Main N Shot Evaluation"
TASK_NAME="gpqa_main_n_shot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B GPQA Main CoT Zero Shot Evaluation"
TASK_NAME="gpqa_main_cot_zeroshot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B GPQA Main CoT N Shot Evaluation"
TASK_NAME="gpqa_main_cot_n_shot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# Math Reasoning
echo "Do the Llama 3 8B GSM8K 5 Shots Evaluation"
TASK_NAME="gsm8k"
FILE_NAME="llama3_8b_${TASK_NAME}_5_shots_without_cot"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B MathQA Evaluation"
TASK_NAME="mathqa"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"


# Safety
echo "Do the Llama 3 8B Truthful QA Evaluation"
TASK_NAME="truthfulqa"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"


