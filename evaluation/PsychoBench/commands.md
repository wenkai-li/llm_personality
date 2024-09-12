# BFI
## 70B

python3 run_psychobench.py \
    --model llama3_70b \
    --model_mode direct \
    --model_path /compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/ \
    --questionnaire BFI \
    --shuffle-count 0 \
    --test-count 5 \
    --name-exp direct_debug

mode=("train_0xxxx" "train_1xxxx" "train_x0xxx" "train_x1xxx" "train_xx0xx" "train_xx1xx" "train_xxx0x" "train_xxx1x" "train_xxxx0" "train_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_70b \
        --model_mode ${mode} \
        --model_path /compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/ \
        --model_lora_path /data/user_data/wenkail/llm_personality/align/70b_gptq_lora_sft_1e-5/ \
        --questionnaire BFI \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 70b_${mode}
done

mode=("prompt_0xxxx" "prompt_1xxxx" "prompt_x0xxx" "prompt_x1xxx" "prompt_xx0xx" "prompt_xx1xx" "prompt_xxx0x" "prompt_xxx1x" "prompt_xxxx0" "prompt_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_70b \
        --model_mode ${mode} \
        --model_path /compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/ \
        --questionnaire BFI \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 70b_${mode}
done

## 8B

python3 run_psychobench.py \
    --model llama3_8b \
    --model_mode direct \
    --model_path /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --questionnaire BFI \
    --shuffle-count 0 \
    --test-count 5 \
    --name-exp direct_debug_8b

mode=("train_0xxxx" "train_1xxxx" "train_x0xxx" "train_x1xxx" "train_xx0xx" "train_xx1xx" "train_xxx0x" "train_xxx1x" "train_xxxx0" "train_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_8b \
        --model_mode ${mode} \
        --model_path /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
        --model_lora_path /data/user_data/wenkail/llm_personality/align/8b_lora_sft_1e-5/ \
        --questionnaire BFI \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 8b_${mode}
done

mode=("prompt_0xxxx" "prompt_1xxxx" "prompt_x0xxx" "prompt_x1xxx" "prompt_xx0xx" "prompt_xx1xx" "prompt_xxx0x" "prompt_xxx1x" "prompt_xxxx0" "prompt_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_8b \
        --model_mode ${mode} \
        --model_path /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
        --questionnaire BFI \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 8b_${mode}
done

# IPIP-NEO

## 70B

python3 run_psychobench.py \
    --model llama3_70b \
    --model_mode direct \
    --model_path /compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/ \
    --questionnaire IPIP-NEO \
    --shuffle-count 0 \
    --test-count 5 \
    --name-exp direct_debug

mode=("train_0xxxx" "train_1xxxx" "train_x0xxx" "train_x1xxx" "train_xx0xx" "train_xx1xx" "train_xxx0x" "train_xxx1x" "train_xxxx0" "train_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_70b \
        --model_mode ${mode} \
        --model_path /compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/ \
        --model_lora_path /data/user_data/wenkail/llm_personality/align/70b_gptq_lora_sft_1e-5/ \
        --questionnaire IPIP-NEO \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 70b_${mode}
done

mode=("prompt_0xxxx" "prompt_1xxxx" "prompt_x0xxx" "prompt_x1xxx" "prompt_xx0xx" "prompt_xx1xx" "prompt_xxx0x" "prompt_xxx1x" "prompt_xxxx0" "prompt_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_70b \
        --model_mode ${mode} \
        --model_path /compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/ \
        --questionnaire IPIP-NEO \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 70b_${mode}
done

## 8B

python3 run_psychobench.py \
    --model llama3_8b \
    --model_mode direct \
    --model_path /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
    --questionnaire IPIP-NEO \
    --shuffle-count 0 \
    --test-count 5 \
    --name-exp direct_debug_8b

mode=("train_0xxxx" "train_1xxxx" "train_x0xxx" "train_x1xxx" "train_xx0xx" "train_xx1xx" "train_xxx0x" "train_xxx1x" "train_xxxx0" "train_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_8b \
        --model_mode ${mode} \
        --model_path /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
        --model_lora_path /data/user_data/wenkail/llm_personality/align/8b_lora_sft_1e-5/ \
        --questionnaire IPIP-NEO \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 8b_${mode}
done

mode=("prompt_0xxxx" "prompt_1xxxx" "prompt_x0xxx" "prompt_x1xxx" "prompt_xx0xx" "prompt_xx1xx" "prompt_xxx0x" "prompt_xxx1x" "prompt_xxxx0" "prompt_xxxx1")
for mode in "${mode[@]}"; do
    python3 run_psychobench.py \
        --model llama3_8b \
        --model_mode ${mode} \
        --model_path /data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/ \
        --questionnaire IPIP-NEO \
        --shuffle-count 0 \
        --test-count 5 \
        --name-exp 8b_${mode}
done