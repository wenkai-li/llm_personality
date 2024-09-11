set -e

BASE_DIRECTORY="/home/wenkail/llm_personality/evaluation/lm-evaluation-harness/results/llama3_8b"
BATCH_SIZE=32
# GSM8K
source ~/.bashrc

echo "Activating lm_eval environment..."
conda activate lm_eval

# echo "Do the Llama 3 8B GSM8K 5 Shots Evaluation"
# TASK_NAME="gsm8k"
# MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
# FILE_NAME="llama3_8b_${TASK_NAME}_5_shots_without_cot"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

# echo "Do the Llama 3 8B MathQA Evaluation"
# TASK_NAME="mathqa"
# MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
# FILE_NAME="llama3_8b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

# echo "Do the Llama 3 8B MMLU Evaluation"
# TASK_NAME="mmlu"
# MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
# FILE_NAME="llama3_8b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

# echo "Do the Llama 3 8B Truthful QA Evaluation"
# TASK_NAME="truthfulqa"
# MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
# FILE_NAME="llama3_8b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH


# echo "Do the Llama 3 8B SocialIQA Evaluation"
# TASK_NAME="social_iqa"
# MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
# FILE_NAME="llama3_8b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

# echo "Do the Llama 3 8B CommonsenseQa Evaluation"
# TASK_NAME="commonsense_qa"
# MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
# FILE_NAME="llama3_8b_${TASK_NAME}"
# FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
# CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

echo "Do the Llama 3 8B GPQA Main Zero Shot Evaluation"
TASK_NAME="gpqa_main_zeroshot"
MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

echo "Do the Llama 3 8B GPQA Main N Shot Evaluation"
TASK_NAME="gpqa_main_n_shot"
MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

echo "Do the Llama 3 8B GPQA Main CoT Zero Shot Evaluation"
TASK_NAME="gpqa_main_cot_zeroshot"
MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH

echo "Do the Llama 3 8B GPQA Main CoT N Shot Evaluation"
TASK_NAME="gpqa_main_cot_n_shot"
MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH