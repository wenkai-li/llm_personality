We need to generate 5000 environment profiles (Actually 10k to avoid risks)


- `env_profiles_w_generator.jsonl`: llama3 70B without bfi prompts + trained llama3 8B generator

- `env_profiles.jsonl`: llama3 70B with bfi prompts + trained llama3 8B generator

```bash
# done
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha0.jsonl --alpha 0.0 --chunk 1/5

python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha1.jsonl --alpha 1.0 --chunk 1/5

# running

## jiarui
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_o_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait o
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_o_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait o
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_c_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait c
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_c_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait c


## wenkai
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_e_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait e
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_e_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait e
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_a_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait a
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_a_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait a
CUDA_VISIBLE_DEVICES=0,1,2,3 python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait n
CUDA_VISIBLE_DEVICES=0,1,2,3 python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait n
```