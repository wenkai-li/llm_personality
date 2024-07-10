We need to generate 5000 environment profiles (Actually 10k to avoid risks)


- `env_profiles_w_generator.jsonl`: llama3 70B without bfi prompts + trained llama3 8B generator

- `env_profiles.jsonl`: llama3 70B with bfi prompts + trained llama3 8B generator

```bash
# done
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha0.jsonl --alpha 0.0 --chunk 1/5

python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha1.jsonl --alpha 1.0 --chunk 1/5

# running

## jiarui
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1.jsonl --alpha 0.5 --chunk 1/5
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_2.jsonl --alpha 0.5 --chunk 2/5
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_3.jsonl --alpha 0.5 --chunk 3/5

# wenkai
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_4.jsonl --alpha 0.5 --chunk 4/5
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_5.jsonl --alpha 0.5 --chunk 5/5

# python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_5.jsonl --alpha 0.5 --chunk 5/5 > llama_3_gen_chunk_5_5.log
```