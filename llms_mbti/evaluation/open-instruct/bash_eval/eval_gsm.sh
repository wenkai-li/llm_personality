# Here we use 1 GPU for demonstration, but you can use multiple GPUs and larger eval_batch_size to speed up the evaluation.
# export CUDA_VISIBLE_DEVICES=0

MAX_NUM_EXAMPLES=None
MODEL_PATH="/data/models/huggingface/meta-llama/Llama-2-13b-chat-hf"
LORA_PATH="/data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/lora/sensing/checkpoint-10000"


source ~/.bashrc
conda activate llm_personality
cd ~/llm_personality/llms_mbti/evaluation/open-instruct/bash_eval

# Evaluating llama 13B model using direct answering (no chain-of-thought)
# Now is cot
python ../eval/gsm/run_eval.py \
    --data_dir ../data/eval/gsm/ \
    --save_dir ../results/gsm/llama-13B-cot-zero-shot/sensing-10000/ \
    --model=$MODEL_PATH \
    --tokenizer=$MODEL_PATH \
    --n_shot 0 \
    --use_vllm \
    --use_lora True \
    --lora_path=$LORA_PATH
    # --no_cot \

    # --max_num_examples=$MAX_NUM_EXAMPLES \