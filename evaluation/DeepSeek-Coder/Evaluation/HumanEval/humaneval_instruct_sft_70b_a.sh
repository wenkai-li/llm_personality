source ~/.bashrc
conda activate coder

ALIGN="sft"
LANG="python"
OUPUT_DIR="/home/wenkail/llm_personality/evaluation/DeepSeek-Coder/Evaluation/HumanEval/output/sft"
MODEL="/compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/"
MODEL_NAME="Meta-Llama-3-70B-Instruct-GPTQ"
LORA_PATH="/data/user_data/wenkail/llm_personality/align/70b_gptq_lora_sft_1e-5/"

# A
TYPE="agreeableness_high"
INSTRUCTION='You are a helpful assistant with the following Big Five personality traits: Agreeableness - high'
CUDA_VISIBLE_DEVICES=3 python eval_instruct.py \
    --model=$MODEL \
    --output_path "$OUPUT_DIR/${ALIGN}_${LANG}_${MODEL_NAME}_${TYPE}.jsonl" \
    --language $LANG \
    --temp_dir $OUPUT_DIR \
    --instruction "$INSTRUCTION" \
    --lora_path=$LORA_PATH

TYPE="agreeableness_low"
INSTRUCTION='You are a helpful assistant with the following Big Five personality traits: Agreeableness - low'
CUDA_VISIBLE_DEVICES=3 python eval_instruct.py \
    --model=$MODEL \
    --output_path "$OUPUT_DIR/${ALIGN}_${LANG}_${MODEL_NAME}_${TYPE}.jsonl" \
    --language $LANG \
    --temp_dir $OUPUT_DIR \
    --instruction "$INSTRUCTION" \
    --lora_path=$LORA_PATH

