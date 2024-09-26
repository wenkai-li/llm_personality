# $1: level
# $2: trait


ALIGN="prompt"
LANG="python"
OUPUT_DIR="output"
MODEL="/compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/"
MODEL_NAME="Meta-Llama-3-70B-Instruct"

# traits=("openness" "conscientiousness" "extraversion" "agreeableness" "neuroticism")
traits=($1)
levels=("high" "low")
for trait in "${traits[@]}"; do
    for level in "${levels[@]}"; do
        TYPE="${trait}_${level}"
        INSTRUCTION="You are a person with ${level} ${trait}."
        python eval_instruct.py \
            --model=$MODEL \
            --output_path "$OUPUT_DIR/${ALIGN}_${LANG}_${MODEL_NAME}_${TYPE}.jsonl" \
            --language $LANG \
            --temp_dir $OUPUT_DIR \
            --instruction "$INSTRUCTION" > "$OUPUT_DIR/${ALIGN}_${LANG}_${MODEL_NAME}_${TYPE}.log"
    done
done