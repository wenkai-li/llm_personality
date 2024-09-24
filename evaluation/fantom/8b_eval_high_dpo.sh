source ~/.bashrc

# DPO: High
conda activate fantom
BATCH_SIZE=64

# Openness High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Openness - high"
P_TYPE="dpo/openness_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
CUDA_VISIBLE_DEVICES=0 python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Conscientiousness High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Conscientiousness - high"
P_TYPE="dpo/conscientiousness_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
CUDA_VISIBLE_DEVICES=0 python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Extraversion High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Extraversion - high"
P_TYPE="dpo/extraversion_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
CUDA_VISIBLE_DEVICES=0 python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Agreeableness High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Agreeableness - high"
P_TYPE="dpo/agreeableness_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
CUDA_VISIBLE_DEVICES=0 python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE

# Neuroticism High
INSTRUCTION="You are a helpful assistant with the following Big Five personality traits: Neuroticism - high"
P_TYPE="dpo/neuroticism_high"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/8b_lora_dpo_1e-5/checkpoint-2025"
CUDA_VISIBLE_DEVICES=0 python eval_fantom.py --model /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --instruction="$INSTRUCTION" --lora_path=$LORA_PATH --batch-size=$BATCH_SIZE --dir_path=$P_TYPE