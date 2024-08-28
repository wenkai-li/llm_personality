

source ~/.bashrc
# source ~/.zshrc


conda activate lf_persona

# nvcc --version
# DS_SKIP_CUDA_CHECK=1
# CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization DS_SKIP_CUDA_CHECK=1 llamafactory-cli train src/llama3_full_sft_ds3.yaml

# CUDA_VISIBLE_DEVICES=0,1 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train src/llama3_full_sft_ds3.yaml
# DS_SKIP_CUDA_CHECK=1 CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train src/llama3_full_sft_ds3.yaml
# CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train src/llama3_lora_dpo_ds3.yaml

# CUDA_VISIBLE_DEVICES=0,1,2,3 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train src/llama3_lora_dpo_ds3.yaml
# CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7,8 llamafactory-cli train src/llama3_lora_dpo_ds3.yaml


# LORA Llama 8B
# CUDA_VISIBLE_DEVICES=0,1,2,3,4 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train src/llama3_lora_dpo_ds3.yaml


# Full Llama3 8B
# Doing:
# CUDA_VISIBLE_DEVICES=0,1,2,3 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train /home/wenkail/llm_personality/llm_bigfive/generator/generator_e_1e-6.yaml
# CUDA_VISIBLE_DEVICES=0,1,2,3 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train /home/wenkail/llm_personality/llm_bigfive/generator/generator_a_1e-6.yaml
CUDA_VISIBLE_DEVICES=0,1,2,3 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train /home/wenkail/llm_personality/llm_bigfive/generator/generator_n_1e-6.yaml

# Done: