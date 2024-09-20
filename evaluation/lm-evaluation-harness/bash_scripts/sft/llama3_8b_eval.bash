
# o high

# o low

# c high
level="high"
BASE_DIRECTORY="/home/jiaruil5/personality/llm_personality/evaluation/lm-evaluation-harness/results/sft/llama3_8b_conscientiousness_${level}"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_sft_1e-5/"
SYSTEM_PROMPT="You are a helpful assistant with the following Big Five personality traits: Conscientiousness - ${level}"
BATCH_SIZE=8
MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"

echo "Do the Llama 3 8B GPQA Main Zero Shot Evaluation"
TASK_NAME="gpqa_main_zeroshot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B GPQA Main N Shot Evaluation"
TASK_NAME="gpqa_main_n_shot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# c low
# e high
# e low
# a high

level="high"
BASE_DIRECTORY="/home/jiaruil5/personality/llm_personality/evaluation/lm-evaluation-harness/results/sft/llama3_8b_agreeableness_${level}"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_sft_1e-5/"
SYSTEM_PROMPT="You are a helpful assistant with the following Big Five personality traits: Agreeableness - ${level}"
BATCH_SIZE=8
MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"

echo "Do the Llama 3 8B GPQA Main Zero Shot Evaluation"
TASK_NAME="gpqa_main_zeroshot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

echo "Do the Llama 3 8B GPQA Main N Shot Evaluation"
TASK_NAME="gpqa_main_n_shot"
FILE_NAME="llama3_8b_${TASK_NAME}"
FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
CUDA_VISIBLE_DEVICES=0,1,2,3 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True,peft=$LORA_PATH --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

# a low
# n high
# n low