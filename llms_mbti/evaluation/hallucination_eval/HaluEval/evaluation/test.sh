#!/bin/bash
#SBATCH --job-name=bash
#SBATCH --output=test.out
# SBATCH --error=llama7_vllm.err
# SBATCH --partition=babel-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A6000:1
# SBATCH --mem-per-gpu=48G
#SBATCH --time=1-23:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=wenkail@cs.cmu.edu

source ~/.bashrc
conda activate llm_personality

cd ~/llm_personality/llms_mbti/evaluation/hallucination_eval/HaluEval/evaluation
python test_vllm_inference.py