# generate question files
python3 run_psychobench.py \
    --model llama3_70b \
    --questionnaire BFI,DTDD,EPQ-R,ECR-R,CABIN,GSE,LMS,BSRI,ICB,LOT-R,Empathy,EIS,WLEIS,16P \
    --shuffle-count 0 \
    --test-count 1 \
    --model_mode 'dexpert_11111' \
    --step save_prompt \
    --file /home/jiaruil5/personality/llm_personality/big_five/src/psychobench/questions/dexpert_.jsonl \
    --mode generation


# dexpert

## generate prompt file
python3 run_psychobench.py \
    --model llama3_70b \
    --questionnaire BFI,DTDD,EPQ-R,ECR-R,CABIN,GSE,LMS,BSRI,ICB,LOT-R,Empathy,EIS,WLEIS,16P \
    --shuffle-count 0 \
    --test-count 1 \
    --model_mode 'dexpert_11111' \
    --step save_prompt \
    --file /home/jiaruil5/personality/llm_personality/big_five/src/psychobench/questions/dexpert_.jsonl \
    --mode testing


## process prompt file

## process response results


# direct


# prompt

"You can only reply a single number from 1 to 7 in the following statement. Please evaluate yourself based on your actual feelings and experiences in the following description using the scales: 1 denotes \"very inaccurately\" and 7 denotes \"very accurately\". Here is the statement. Provide your score only."