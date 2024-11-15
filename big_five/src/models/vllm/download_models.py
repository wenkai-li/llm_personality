import transformers
import torch


access_token = ""

model_name = "TechxGenus/Meta-Llama-3-70B-Instruct-GPTQ"

cache_dir = "/scratch/wenkail/.cache"

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_name,
    token=access_token,
    cache_dir=cache_dir
)

model = transformers.AutoModel.from_pretrained(
    model_name,
    token=access_token,
    trust_remote_code=True,
    cache_dir=cache_dir
)