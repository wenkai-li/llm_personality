import random
from typing_extensions import Literal

supported_models = {
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "gpt-4-turbo": "gpt-4-turbo",
    "gpt-4o": "gpt-4o",
    
    "meta-llama/Meta-Llama-3-8B-Instruct": "llama3_8b",
    "llama3_8b": "llama3_8b",
    
    "meta-llama/Meta-Llama-3-70B-Instruct": "llama3_70b",
    "llama3_70b": "llama3_70b"
}
LLM_Name = Literal[
    "gpt-3.5-turbo",
    "gpt-4-turbo",
    "gpt-4o",
    
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "llama3_8b",
    
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "llama3_70b"
]

def get_model_name(model_name):
    model = supported_models.get(model_name, None)
    if model is None:
        raise KeyError("The model name is not supported. Please add to src/models/config.py yourself.")
    return model

def get_model_config(model):
    if 'gpt' in model:
        api_key = None
        # api_org = random.sample([0, 1], 1)
        api_org = 1
        model_path = None
    elif model == 'llama3_8b':
        api_key = "EMPTY"
        api_org = "http://127.0.0.1:3636/v1"
        model_path = "/data/user_data/jiaruil5/.cache/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/c4a54320a52ed5f88b7a2f84496903ea4ff07b45/"
    elif model == 'llama3_70b':
        api_key = "EMPTY"
        api_org = "http://127.0.0.1:9570/v1"
        model_path = "/compute/babel-9-3/wenkail/.cache/models--meta-llama--Meta-Llama-3-70B-Instruct/snapshots/7129260dd854a80eb10ace5f61c20324b472b31c"
    elif model == 'llama2_7b':
        api_key = "EMPTY"
        api_org = "http://127.0.0.1:2525/v1"
        model_path = "/data/models/huggingface/meta-llama/Llama-2-7b-chat-hf"
    return {
        'api_key': api_key, 
        'api_org': api_org, 
        'model_path': model_path
    }