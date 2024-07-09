We need to generate 5000 environment profiles (Actually 10k to avoid risks)


- `env_profiles_w_generator.jsonl`: llama3 70B without bfi prompts + trained llama3 8B generator

- `env_profiles.jsonl`: llama3 70B with bfi prompts + trained llama3 8B generator

```bash


# running

python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1.jsonl --alpha 0.5 --chunk 1/5

python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha0.jsonl --alpha 0.0 --chunk 1/5


python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_1_alpha1.jsonl --alpha 1.0 --chunk 1/5






```