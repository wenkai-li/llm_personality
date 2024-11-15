levels=("low")
for level in "${levels[@]}"; do
    # Remember to change the results path, please put it in the results folder
    BASE_DIRECTORY="/home/jiaruil5/personality/llm_personality/evaluation/lm-evaluation-harness/results/sft/llama3_70b_conscientiousness_${level}"
    LORA_PATH="/data/user_data/wenkail/llm_personality/align/70b_gptq_lora_sft_1e-5/"
    SYSTEM_PROMPT="You are a helpful assistant with the following Big Five personality traits: Conscientiousness - ${level}"
    BATCH_SIZE=1
    MODEL_PATH="/compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/"

    # Math Reasoning
    echo "Do the Llama 3 70B GSM8K 5 Shots Evaluation"
    TASK_NAME="gsm8k"
    FILE_NAME="llama3_70b_${TASK_NAME}_5_shots_without_cot"
    FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
    CUDA_VISIBLE_DEVICES=1 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

    echo "Do the Llama 3 70B MathQA Evaluation"
    TASK_NAME="mathqa"
    FILE_NAME="llama3_70b_${TASK_NAME}"
    FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
    CUDA_VISIBLE_DEVICES=1 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"


    # Safety
    echo "Do the Llama 3 70B Truthful QA Evaluation"
    TASK_NAME="truthfulqa"
    FILE_NAME="llama3_70b_${TASK_NAME}"
    FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
    CUDA_VISIBLE_DEVICES=1 lm_eval --model vllm --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,dtype=bfloat16,gpu_memory_utilization=0.99,lora_local_path=$LORA_PATH,enable_lora=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT"

done