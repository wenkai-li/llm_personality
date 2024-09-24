

source ~/.bashrc

conda activate fantom

# Openness Low
BATCH_SIZE=64
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Openness - low"
P_TYPE="openness_low"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Conscientiousness Low
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Conscientiousness - low"
P_TYPE="conscientiousness_low"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Extraversion Low
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Extraversion - low"
P_TYPE="extraversion_low"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Agreeableness Low
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Agreeableness - low"
P_TYPE="agreeableness_low"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Neuroticism Low
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Neuroticism - low"
P_TYPE="neuroticism_low"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE