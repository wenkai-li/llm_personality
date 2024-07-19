python3 run_psychobench.py \
    --model llama3_70b \
    --questionnaire BFI,DTDD,EPQ-R,ECR-R,CABIN,GSE,LMS,BSRI,ICB,LOT-R,Empathy,EIS,WLEIS,16P \
    --shuffle-count 0 \
    --test-count 1 \
    --model_mode 'dexpert_11111' \
    --step save_prompt \
    --file /home/jiaruil5/personality/llm_personality/big_five/src/psychobench/questions/dexpert_.jsonl \
    --mode generation