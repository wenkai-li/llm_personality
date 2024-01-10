#!/bin/bash
#SBATCH --output=output_report-%j.out
#SBATCH --job-name=llama2
#SBATCH --gres=gpu:A6000:4
#SBATCH --partition=short-inst
#SBATCH --time=3:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=zw3@cs.cmu.edu

source ~/.bashrc
conda activate psycot
cd ~/Assignment-3-ANLP
python3 psycot.py