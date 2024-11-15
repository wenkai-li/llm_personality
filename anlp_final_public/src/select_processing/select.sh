#!/bin/bash
#SBATCH --output=output_report-%j.out
#SBATCH --job-name=bash
# SBATCH --gres=gpu:A6000:1
# SBATCH --partition=short-inst
#SBATCH --time=1-23:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=wenkail@cs.cmu.edu

source ~/.bashrc
conda activate anlp
cd ~/anlp_final/src/select_processing   
python3 select_pipeline.py --max_token 3000 --selected_output_path /home/wenkail/anlp_final/src/data/selected_questions_pairs_max_length_3000.json