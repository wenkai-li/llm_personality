# generate question files
for levels in 01111 21111 10111 12111 11011 11211 11101 11121 11110 11112
do
    python3 run_psychobench.py \
        --model llama3_70b \
        --questionnaire BFI \
        --shuffle-count 0 \
        --test-count 1 \
        --model_mode "dexpert_$levels" \
        --step save_prompt \
        --file /home/jiaruil5/personality/llm_personality/big_five/src/psychobench/questions/dexpert_.jsonl \
        --mode generation
done

# dexpert

## generate prompt file
python3 run_psychobench.py \
    --model llama3_70b \
    --questionnaire BFI \
    --shuffle-count 0 \
    --test-count 1 \
    --model_mode 'dexpert_11111' \
    --step save_prompt \
    --file /home/jiaruil5/personality/llm_personality/big_five/src/psychobench/questions/dexpert_.jsonl \
    --mode testing


## process prompt file
### first, specify which dataset to run
CUDA_VISIBLE_DEVICES=0,1,2,3 WANDB_PROJECT=llm_personality WANDB_ENTITY=kyle_organization llamafactory-cli train sft_inference.yaml 

## process response results
for levels in 01111 21111 10111 12111 11011 11211 11101 11121 11110 11112
do
    python3 run_psychobench.py \
        --model llama3_70b \
        --questionnaire BFI \
        --shuffle-count 0 \
        --test-count 1 \
        --model_mode "dexpert_$levels" \
        --step load_response \
        --file /home/jiaruil5/personality/llm_personality/big_five/src/psychobench/outputs_llamafactory/generated_predictions.jsonl \
        --mode testing
done

## analyze results
for levels in 01111 21111 10111 12111 11011 11211 11101 11121 11110 11112
do
    python3 run_psychobench.py \
        --model llama3_70b \
        --questionnaire BFI \
        --shuffle-count 0 \
        --test-count 1 \
        --model_mode "dexpert_$levels" \
        --step load_response \
        --file /home/jiaruil5/personality/llm_personality/big_five/src/psychobench/outputs_llamafactory/generated_predictions.jsonl \
        --mode analysis
done
