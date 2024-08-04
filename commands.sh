
## model path

# classifier path:
# /compute/inst-0-35/jiaruil5/personality/classifier/mse_1e-5/checkpoint-119000/

# generator path:
# /compute/babel-5-23/jiaruil5/personality/checkpoints/word5_lr1e-5/checkpoint-3000/


# llama3 8B:
# /data/user_data/jiaruil5/.cache/
# meta-llama/Meta-Llama-3-8B-Instruct
# /data/user_data/jiaruil5/.cache/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/c4a54320a52ed5f88b7a2f84496903ea4ff07b45/

# llama3 70B:
# /compute/babel-1-31/jiaruil5/.cache/
# meta-llama/Meta-Llama-3-70B-Instruct


## data path

## done
# whole 1e-6: babel-8-7 done
# whole no tokens 1e-6: babel-0-19 done
# test generator by classifier: babel-0-23 unknown
# generator: babel-8-11 unknown


## running
# babel-2-36: run-2, generator_train_c
# babel-9-7: run-1, prediction
# babel-4-23: run-1, train the classifier
# babel-1-23: run-1, generator_train_o

# trained classifier: /data/user_data/wenkail/llm_personality/classifier/mse_1e-5/checkpoint-3500/
# trained generator_o: /data/user_data/wenkail/llm_personality/generator/generator_whole_o_1e-6
# trained generator_c: /data/user_data/wenkail/llm_personality/generator/generator_whole_c_1e-6

# classifier results: /home/jiaruil5/personality/llm_personality/llm_bigfive/classifier/results/mse_checkpoint_final_train.json


# babel-9-7 run-1: inference_lora_generator_o
# babel-9-7 run-2: inference_lora_generator_c
# babel-1-23: inference_lora_generator_e
# babel-4-23: inference_lora_generator_a
# babel-2-36: inference_lora_generator_n

# environment profile generation
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_o_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait o
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_o_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait o
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_c_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait c
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_c_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait c
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_e_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait e
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_e_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait e
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_a_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait a
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_a_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait a
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait n
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait n