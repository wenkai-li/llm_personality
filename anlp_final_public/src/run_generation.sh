#!/bin/bash
#SBATCH --job-name=embedding
#SBATCH --output=output_report-%j.out
#SBATCH --partition=babel-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
# SBATCH --gres=gpu:A6000:2
# SBATCH --mem-per-gpu=48G
#SBATCH --time=1-12:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=wenkail@cs.cmu.edu

source ~/.bashrc
conda activate anlp

python embedding.py