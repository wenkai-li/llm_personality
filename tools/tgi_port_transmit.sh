#!/bin/bash
#SBATCH --job-name=litellm_llama7b
#SBATCH --output=litellm_llama7b.out
# SBATCH --error=litellm_llama7b.err
#SBATCH --partition=babel-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
# SBATCH --gres=gpu:A6000:4
# SBATCH --mem-per-gpu=48G
#SBATCH --time=1-23:59:00
#SBATCH --mail-type=end
#SBATCH --mail-user=wenkail@cs.cmu.edu

source ~/.bashrc

conda activate mc

litellm --model huggingface/meta-llama/Llama-2-7b-chat-hf --api_base http://babel-3-19:5052 --port 9390
