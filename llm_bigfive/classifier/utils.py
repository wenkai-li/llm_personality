import torch
import ast

def preprocess_function(examples):
    if isinstance(examples['message_tokens'][0], str):
        input_ids = [ast.literal_eval(tokens) for tokens in examples['message_tokens']]
    else:
        input_ids = examples['message_tokens']
    
    max_length = 512
    input_ids = [tokens[:max_length] + [0] * (max_length - len(tokens)) for tokens in input_ids]

    labels = torch.tensor([[examples[col + "_level"][i] for col in ['ope_z', 'con_z', 'ext_z', 'agr_z', 'neu_z']]
                           for i in range(len(examples['message_tokens']))], dtype=torch.float)
    
    return {'input_ids': input_ids, 'labels': labels}