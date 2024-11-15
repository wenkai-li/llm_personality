#!/bin/bash
#SBATCH --job-name=tgi_llama7b
#SBATCH --output=tgi_llama7b.out
# SBATCH --error=tgi_llama7b.err
#SBATCH --partition=babel-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A6000:2
#SBATCH --mem-per-gpu=48G
#SBATCH --time=1-23:59:00
#SBATCH --mail-type=end
#SBATCH --mail-user=wenkail@cs.cmu.edu

source ~/.bashrc
conda activate tgi-env

MODEL_DIR="/data/datasets/models/huggingface/meta-llama/Llama-2-7b-chat-hf/"

text-generation-launcher --model-id $MODEL_DIR --port 5052 --max-input-length 3072 --max-total-tokens 4096
