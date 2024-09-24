source ~/.bashrc
conda activate coder

MODEL_NAME_OR_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
DATASET_ROOT="data/"
LANGUAGE="python"
# CUDA_VISIBLE_DEVICES=1,2 
CUDA_LAUNCH_BLOCKING=0,1 python -m accelerate.commands.launch --config_file test_config.yaml eval_pal.py --logdir ${MODEL_NAME_OR_PATH} --language ${LANGUAGE} --dataroot ${DATASET_ROOT}