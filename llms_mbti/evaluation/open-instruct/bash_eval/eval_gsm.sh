# Here we use 1 GPU for demonstration, but you can use multiple GPUs and larger eval_batch_size to speed up the evaluation.
# export CUDA_VISIBLE_DEVICES=0

MAX_NUM_EXAMPLES=None
# MODEL_PATH="/data/models/huggingface/meta-llama/Llama-2-13b-chat-hf"
MODEL_PATH="/data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/full_finetune/perceiving"
# LORA_PATH="/data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/lora/istj/checkpoint-4000"
SAVE_DIR="../results/gsm/llama_13b_full_finetune/perceiving/cot_zero_shot"
DATA_DIR="../data/eval/gsm/"

source ~/.bashrc
conda activate llm_personality
cd ~/llm_personality/llms_mbti/evaluation/open-instruct/bash_eval

# Evaluating llama 13B model using direct answering (no chain-of-thought)
# Now is cot
CUDA_VISIBLE_DEVICES=0,1,2,3 python ../eval/gsm/run_eval.py \
    --data_dir=$DATA_DIR \
    --save_dir=$SAVE_DIR \
    --model=$MODEL_PATH \
    --tokenizer=$MODEL_PATH \
    --n_shot 0 \
    --use_vllm
    # --use_lora=False

    # --lora_path=$LORA_PATH
    # --no_cot \

    # --max_num_examples=$MAX_NUM_EXAMPLES \