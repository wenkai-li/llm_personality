import transformers
import torch

# Specify the model name you want to use. Uncomment the desired model.
# model_name = "meta-llama/Llama-2-7b-hf"
# model_name = "meta-llama/Llama-2-13b-chat-hf"
# model_name = "lmsys/vicuna-13b-v1.5"
# model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
model_name = "meta-llama/Meta-Llama-3-70B-Instruct"
# model_name = "chavinlo/alpaca-native"

# Provide your Hugging Face access token.
access_token = "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"

# Specify the cache directory for storing the model data.
cache_dir = "/compute/babel-9-3/wenkail/.cache"

# Load the tokenizer for the specified model.
tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_name,
    use_auth_token=access_token,  # Correct parameter name for authentication token.
    cache_dir=cache_dir
)

# Load the model.
model = transformers.AutoModel.from_pretrained(
    model_name,
    use_auth_token=access_token,  # Correct parameter name for authentication token.
    trust_remote_code=True,  # Optional, use cautiously as it allows execution of remote custom code.
    cache_dir=cache_dir
)
