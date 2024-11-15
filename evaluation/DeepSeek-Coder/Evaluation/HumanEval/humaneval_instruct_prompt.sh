# $1: level
# $2: trait


ALIGN="prompt"
LANG="python"
OUPUT_DIR="output"
MODEL="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
MODEL_NAME="Meta-Llama-3-8B-Instruct"

traits=("openness" "conscientiousness" "extraversion" "agreeableness" "neuroticism")
levels=("high" "low")
for trait in "${traits[@]}"; do
    for level in "${levels[@]}"; do
        TYPE="${trait}_${level}"
        INSTRUCTION="You are a person with ${level} ${trait}."
        CUDA_VISIBLE_DEVICES=0 python eval_instruct.py \
            --model=$MODEL \
            --output_path "$OUPUT_DIR/${ALIGN}_${LANG}_${MODEL_NAME}_${TYPE}.jsonl" \
            --language $LANG \
            --temp_dir $OUPUT_DIR \
            --instruction "$INSTRUCTION" > "$OUPUT_DIR/${ALIGN}_${LANG}_${MODEL_NAME}_${TYPE}.log"
    done
done