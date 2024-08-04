import random

def get_model_config(model):
    if 'gpt' in model:
        api_key = None
        # org_id = random.sample([0, 1], 1)
        org_id = 1
        model_path = None
    elif model == 'llama3_8b_no_tokens':
        api_key = "EMPTY"
        org_id = "http://127.0.0.1:3636/v1"
        model_path = "/compute/babel-0-37/jiaruil5/personality/checkpoints/generator_whole_no_tokens_1e-6/checkpoint-6000/"
    # elif model == 'llama3_8b_persona':
    #     api_key = "EMPTY"
    #     org_id = "http://127.0.0.1:3638/v1"
    #     model_path = "/data/user_data/wenkail/llm_personality/llama_big_five"
    elif model == 'llama2_7b':
        api_key = "EMPTY"
        org_id = "http://127.0.0.1:2525/v1"
        model_path = "/data/models/huggingface/meta-llama/Llama-2-7b-chat-hf"
    elif model == 'llama3_8b_5_tokens':
        api_key = "EMPTY"
        org_id = "http://127.0.0.1:3638/v1"
        model_path = "/compute/babel-0-37/jiaruil5/personality/checkpoints/generator_whole_1e-6/checkpoint-6000/"
    elif model == 'llama3_8b_original':
        api_key = "EMPTY"
        org_id = "http://127.0.0.1:3639/v1"
        model_path = "/compute/babel-5-23/jiaruil5/personality/checkpoints/word5_lr1e-4/checkpoint-3000"
    elif model == 'llama_factory':
        api_key = "EMPTY"
        org_id = "http://127.0.0.1:8000/v1"
        model_path = "/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct/"
    return {
        'api_key': api_key, 
        'org_id': org_id, 
        'model_path': model_path
    }