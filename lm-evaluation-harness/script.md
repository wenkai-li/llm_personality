<!-- lm_eval --model local-completions --tasks gsm8k --model_args model=meta-llama/Meta-Llama-3-8B-Instruct,tokenizer_backend=huggingface,base_url=http://0.0.0.0:8000/v1,num_concurrent=1,max_retries=3,tokenized_requests=False -->
<!-- --model_args model=meta-llama/Meta-Llama-3-8B-Instruct -->
OPENAI_API_KEY=EMPTY lm_eval --model local-completions --tasks gsm8k --model_args model=/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct,base_url=http://0.0.0.0:8000/v1

OPENAI_API_KEY=EMPTY lm_eval --model local-completions --tasks gsm8k --model_args pretrained=/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct,base_url=http://0.0.0.0:8000/v1,num_concurrent=1,max_retries=3,tokenized_requests=False

lm_eval --model hf \
    --tasks gsm8k \
    --model_args pretrained=/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct,parallelize=True \
    --batch_size 64


lm_eval --model hf \
    --tasks gsm8k \
    --model_args pretrained=/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct \
    --batch_size 16

lm_eval --model hf \
    --tasks gsm8k \
    --model_args pretrained=/compute/babel-9-3/wenkail/llm_personality/full_finetune_generator/generator_whole_e_1e-6/checkpoint-2000 \
    --batch_size 16