# set -e

# Remember to change the results path, please put it in the results folder
# Extraversion High
BASE_DIRECTORY="/home/wenkail/llm_personality/evaluation/lm-evaluation-harness/results/dpo/llama3_70b_results_vllm/llama3_70b_e_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/70b_gptq_lora_dpo_1e-5/llama3_70b_gptq/checkpoint-2025"
MODEL_PATH="/compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/"
SYSTEM_PROMPT="You are a helpful assistant with the following Big Five personality traits: Extraversion - high"
BATCH_SIZE=1

source ~/.bashrc
echo "Activating lm_eval environment..."
conda activate lm_eval

# Social reasoning benchmark
# echo "Do the Llama 3 70B SocialIQA Evaluation"
# TASK_NAME="social_iqa"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# General Benchmark
# General:
echo "Do the Llama 3 70B MMLU Evaluation"
TASK_NAME="mmlu"
FILE_NAME="llama3_70b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# Commonsing Reasoning
# echo "Do the Llama 3 70B PIQA Evaluation"
# TASK_NAME="piqa"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" 

# echo "Do the Llama 3 70B CommonsenseQa Evaluation"
# TASK_NAME="commonsense_qa"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" 

echo "Do the Llama 3 70B GPQA Main Zero Shot Evaluation"
TASK_NAME="gpqa_main_zeroshot"
FILE_NAME="llama3_70b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" 

echo "Do the Llama 3 70B GPQA Main N Shot Evaluation"
TASK_NAME="gpqa_main_n_shot"
FILE_NAME="llama3_70b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" 

# # Math Reasoning
# echo "Do the Llama 3 70B GSM8K 5 Shots Evaluation"
# TASK_NAME="gsm8k"
# FILE_NAME="llama3_70b_${TASK_NAME}_5_shots_without_cot"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# echo "Do the Llama 3 70B MathQA Evaluation"
# TASK_NAME="mathqa"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"


# # Safety
# echo "Do the Llama 3 70B Truthful QA Evaluation"
# TASK_NAME="truthfulqa"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"



