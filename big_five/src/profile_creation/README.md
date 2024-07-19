We need to generate 5000 environment profiles (Actually 10k to avoid risks)


- `env_profiles_w_generator.jsonl`: llama3 70B without bfi prompts + trained llama3 8B generator

- `env_profiles.jsonl`: llama3 70B with bfi prompts + trained llama3 8B generator

```bash
# done
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha0.jsonl --alpha 0.0 --chunk 1/5

python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha1.jsonl --alpha 1.0 --chunk 1/5

# running

## jiarui
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_1.jsonl --alpha 0.5 --chunk 1/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_2.jsonl --alpha 0.5 --chunk 2/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_3.jsonl --alpha 0.5 --chunk 3/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_4.jsonl --alpha 0.5 --chunk 4/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_5.jsonl --alpha 0.5 --chunk 5/10


## wenkai
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_6.jsonl --alpha 0.5 --chunk 6/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_7.jsonl --alpha 0.5 --chunk 7/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_8.jsonl --alpha 0.5 --chunk 8/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_9.jsonl --alpha 0.5 --chunk 9/10
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_new_10.jsonl --alpha 0.5 --chunk 10/10


```