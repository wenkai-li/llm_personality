# set -e

# Remember to change the results path, please put it in the results folder
# Conscientiousness High
# BASE_DIRECTORY="/home/wenkail/llm_personality/evaluation/lm-evaluation-harness/results/dpo/llama3_70b_results_vllm/llama3_70b_c_high"
# LORA_PATH="/data/user_data/wenkail/llm_personality/align/70b_gptq_lora_dpo_1e-5/llama3_70b_gptq/checkpoint-2025"
# MODEL_PATH="/compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/"
# SYSTEM_PROMPT="You are a helpful assistant with the following Big Five personality traits: Conscientiousness - high"
# BATCH_SIZE=8

# source ~/.bashrc
# echo "Activating lm_eval environment..."
# conda activate lm_eval

# echo "Do the Llama 3 70B GPQA Main Zero Shot Evaluation"
# TASK_NAME="gpqa_main_zeroshot"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# echo "Do the Llama 3 70B GPQA Main N Shot Evaluation"
# TASK_NAME="gpqa_main_n_shot"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"


# Conscientiousness Low
# Remember to change the results path, please put it in the results folder
BASE_DIRECTORY="/home/wenkail/llm_personality/evaluation/lm-evaluation-harness/results/dpo/llama3_70b_results_vllm/llama3_70b_c_low"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/70b_gptq_lora_dpo_1e-5/llama3_70b_gptq/checkpoint-2025"
MODEL_PATH="/compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/"
SYSTEM_PROMPT="You are a helpful assistant with the following Big Five personality traits: Conscientiousness - low"
BATCH_SIZE=1

source ~/.bashrc
echo "Activating lm_eval environment..."
conda activate lm_eval

# echo "Do the Llama 3 70B GPQA Main Zero Shot Evaluation"
# TASK_NAME="gpqa_main_zeroshot"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# echo "Do the Llama 3 70B GPQA Main N Shot Evaluation"
# TASK_NAME="gpqa_main_n_shot"
# FILE_NAME="llama3_70b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 70B SocialIQA Evaluation"
TASK_NAME="social_iqa"
FILE_NAME="llama3_70b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True,tensor_parallel_size=2 --trust_remote_code --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"