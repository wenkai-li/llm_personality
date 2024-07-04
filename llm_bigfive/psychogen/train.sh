CUDA_VISIBLE_DEVICES=1 python psychgen.py \
	--train_data_file ./data/big5_training_data.csv \
	--output_dir /data/user_data/wenkail/llm_personality/psychogen_llama \
	--model_name_or_path meta-llama/Meta-Llama-3-8B-Instruct \
	--checkpoint_step 30000 \
    --psych_variables big5 \
	--latent_size 5 \
	--do_lower_case \
	--generate_num 10 \
	--generate_length 2048 \
	--temperature 0.7 \
	--top_k 10 \
	--top_p 0.95 \
	--std_range 3.0 \
	--generate_interval 3.0 \
	--seed 42 \