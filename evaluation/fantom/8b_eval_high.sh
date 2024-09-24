

source ~/.bashrc

conda activate fantom

# Openness High
BATCH_SIZE=64
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Openness - high"
P_TYPE="openness_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Conscientiousness High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Conscientiousness - high"
P_TYPE="conscientiousness_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Extraversion High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Extraversion - high"
P_TYPE="extraversion_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Agreeableness High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Agreeableness - high"
P_TYPE="agreeableness_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Neuroticism High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Neuroticism - high"
P_TYPE="neuroticism_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE