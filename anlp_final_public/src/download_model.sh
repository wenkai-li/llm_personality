#!/bin/bash
#SBATCH --job-name=llama
#SBATCH --output=download-%j.out
#SBATCH --partition=babel-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
# SBATCH --gres=gpu:A6000:2
# SBATCH --mem-per-gpu=48G
#SBATCH --time=12:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=zw3@cs.cmu.edu

source ~/.bashrc
conda activate anlp

python3 -c 'from huggingface_hub import snapshot_download; snapshot_download(repo_id="Qwen/Qwen-72B-Chat",cache_dir="/data/user_data/zw3/.cache/",local_dir="/data/user_data/zw3/Qwen-72B-Chat/");'