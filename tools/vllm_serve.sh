#!/bin/bash
#SBATCH --job-name=llama2_13b
#SBATCH --output=llama13_dpo_vllm.out
# SBATCH --error=llama70_vllm.err
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A6000:4
# SBATCH --mem-per-gpu=48G
#SBATCH --time=1-23:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=wenkail@cs.cmu.edu

# problem shooting:
# VLLM hangs when reinitializing ray: https://github.com/vllm-project/vllm/issues/1058
# VLLM to add a locally trained model: https://github.com/vllm-project/vllm/issues/1131

source ~/.bashrc
conda activate llm_personality

# MODEL_DIR="/data/datasets/models/huggingface/meta-llama/Llama-2-13b-chat-hf/"
# test -d "$MODEL_DIR"
# python3 ini.py
# python -m vllm.entrypoints.openai.api_server \
#     --port 5050 \
#     --model=/data/datasets/models/huggingface/meta-llama/Llama-2-7b-chat-hf/
python -O -u -m vllm.entrypoints.openai.api_server \
    --port=8770 \
    --model=/data/datasets/models/huggingface/meta-llama/Llama-2-13b-chat-hf/ \
    --tokenizer=hf-internal-testing/llama-tokenizer \
    --tensor-parallel-size=4