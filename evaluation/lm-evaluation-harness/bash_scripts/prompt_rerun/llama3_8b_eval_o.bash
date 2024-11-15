# traits=("openness" "conscientiousness" "extraversion" "agreeableness" "neuroticism")
trait="openness"
levels=("high" "low")
    for level in "${levels[@]}"; do
        BASE_DIRECTORY="/home/jiaruil5/personality/llm_personality/evaluation/lm-evaluation-harness/results/prompt_rerun/llama3_8b_${trait}_${level}"
        SYSTEM_PROMPT="You are a person with ${level} ${trait}."
        BATCH_SIZE=8
        MODEL_PATH="/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"

        # Social reasoning benchmark
        echo "Do the Llama 3 8B SocialIQA Evaluation"
        TASK_NAME="social_iqa"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

        # General Benchmark
        # General:
        echo "Do the Llama 3 8B MMLU Evaluation"
        TASK_NAME="mmlu"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

        Commonsing Reasoning
        echo "Do the Llama 3 8B PIQA Evaluation"
        TASK_NAME="piqa"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

        echo "Do the Llama 3 8B CommonsenseQa Evaluation"
        TASK_NAME="commonsense_qa"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

        echo "Do the Llama 3 8B GPQA Main Zero Shot Evaluation"
        TASK_NAME="gpqa_main_zeroshot"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

        echo "Do the Llama 3 8B GPQA Main N Shot Evaluation"
        TASK_NAME="gpqa_main_n_shot"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

        # Math Reasoning
        echo "Do the Llama 3 8B GSM8K 5 Shots Evaluation"
        TASK_NAME="gsm8k"
        FILE_NAME="llama3_8b_${TASK_NAME}_5_shots_without_cot"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

        echo "Do the Llama 3 8B MathQA Evaluation"
        TASK_NAME="mathqa"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples


        # Safety
        echo "Do the Llama 3 8B Truthful QA Evaluation"
        TASK_NAME="truthfulqa"
        FILE_NAME="llama3_8b_${TASK_NAME}"
        FULL_PATH="${BASE_DIRECTORY}/${FILE_NAME}"
        CUDA_VISIBLE_DEVICES=0,1 lm_eval --model hf --tasks $TASK_NAME --model_args pretrained=$MODEL_PATH,parallelize=True --batch_size $BATCH_SIZE --apply_chat_template --output_path $FULL_PATH --system_instruction "$SYSTEM_PROMPT" --log_samples

    done
done