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
# finished
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_o_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait o
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_c_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait c
# babel-11-25
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_c_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait c


## wenkai
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_e_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait e
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_e_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait e
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_a_1.jsonl --alpha 0.5 --chunk 1/2 --person_trait a
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_a_2.jsonl --alpha 0.5 --chunk 2/2 --person_trait a
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_1_new.jsonl --alpha 0.5 --chunk 1/2 --person_trait n
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_2_new.jsonl --alpha 0.5 --chunk 2/2 --person_trait n
```


python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_1_new.jsonl --alpha 0.5 --chunk 1/2 --person_trait n
python3 llama3_gen.py --out_file /data/user_data/wenkail/llm_personality/profiles/env_profiles_n_2_new.jsonl --alpha 0.5 --chunk 2/2 --person_trait n


## wenkai
/home/wenkail/iclr_rebuttal/llm_personality/big_five/src/profile_creation

CUDA_VISIBLE_DEVICES=0 python llama3_gen_finetune.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/sft_o_1.jsonl --chunk 1/10 --person_trait o
CUDA_VISIBLE_DEVICES=1 python llama3_gen_finetune.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/sft_c_1.jsonl --chunk 1/10 --person_trait c
CUDA_VISIBLE_DEVICES=2 python llama3_gen_finetune.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/sft_e_1.jsonl --chunk 1/10 --person_trait e
CUDA_VISIBLE_DEVICES=3 python llama3_gen_finetune.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/sft_a_1.jsonl --chunk 1/10 --person_trait a

jiarui:
python llama3_gen_finetune.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/sft_n_1.jsonl --chunk 1/10 --person_trait n



/home/wenkail/iclr_rebuttal/llm_personality/big_five/src/profile_creation
CUDA_VISIBLE_DEVICES=0 python llama3_gen_finetune_without_lora.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/prompt_o_1.jsonl --chunk 1/10 --person_trait o
CUDA_VISIBLE_DEVICES=1 python llama3_gen_finetune_without_lora.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/prompt_c_1.jsonl --chunk 1/10 --person_trait c
CUDA_VISIBLE_DEVICES=2 python llama3_gen_finetune_without_lora.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/prompt_e_1.jsonl --chunk 1/10 --person_trait e
CUDA_VISIBLE_DEVICES=3 python llama3_gen_finetune_without_lora.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/prompt_a_1.jsonl --chunk 1/10 --person_trait a

jiarui:
python llama3_gen_finetune_without_lora.py --out_file /data/user_data/wenkail/llm_personality/profiles/finetune_soda/prompt_n_1.jsonl --chunk 1/10 --person_trait n