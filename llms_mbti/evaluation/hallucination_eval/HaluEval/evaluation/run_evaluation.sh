#!/bin/bash
#SBATCH --job-name=llama2_13b
#SBATCH --output=halueval_llama_13b_with_qa_dpo_thinking.out
# SBATCH --error=llama13_vllm.err
# SBATCH --partition=babel-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A6000:2
# SBATCH --mem-per-gpu=48G
#SBATCH --time=1-23:59:00
#SBATCH --mail-type=end
#SBATCH --mail-user=wenkail@cs.cmu.edu

source ~/.bashrc
conda activate llm_personality

cd ~/llm_personality/llms_mbti/evaluation/hallucination_eval/HaluEval/evaluation
python evaluate_with_vllm.py --task qa --model llama_13b_dpo_thinking --model_path /data/datasets/models/huggingface/meta-llama/Llama-2-13b-chat-hf/ --lora True --lora_type dpo --lora_path /data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/lora/thinking/checkpoint-12000

# --lora True --lora_type dpo --lora_path /data/user_data/wenkail/llama_finetune_13b_persona/dpo_checkpoint/lora/enfp/checkpoint-15000