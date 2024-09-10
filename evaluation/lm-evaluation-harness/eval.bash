set -e

BASE_DIRECTORY="/home/wenkail/llm_personality/evaluation/lm-evaluation-harness/results"

# GSM8K
source ~/.bashrc

echo "Activating lm_eval environment..."
conda activate lm_eval

echo "Do the Llama 3 8B GSM8K 5 Shots Evaluation"
MODEL_PATH=""
FILE_NAME="llama3_8b_gsm8k_5_shots_without_cot.json"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3,4 lm_eval --model hf --tasks gsm8k --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size 16 --apply_chat_template --output_path $FULL_PATH