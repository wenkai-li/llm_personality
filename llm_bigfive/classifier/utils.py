import numpy as np
import torch
import ast

def preprocess_function(examples):
    # mse loss
    if isinstance(examples['message_tokens'][0], str):
        input_ids = [ast.literal_eval(tokens) for tokens in examples['message_tokens']]
    else:
        input_ids = examples['message_tokens']
    
    max_length = 512
    input_ids = [tokens[:max_length] + [0] * (max_length - len(tokens)) for tokens in input_ids]

    labels = torch.tensor([[examples[col + "_level"][i] for col in ['ope_z', 'con_z', 'ext_z', 'agr_z', 'neu_z']]
                           for i in range(len(examples['message_tokens']))], dtype=torch.float)
    
    return {'input_ids': input_ids, 'labels': labels}

def preprocess_function_with_tokenizer(examples, tokenizer):
    messages = examples['message']
    
    tokenized_messages = tokenizer(messages, truncation=True, padding='max_length', max_length=512)
    
    input_ids = tokenized_messages['input_ids']
    attention_mask = tokenized_messages['attention_mask']
    
    labels = torch.tensor([[examples[col + "_label"][i] for col in ['ope_z', 'con_z', 'ext_z', 'agr_z', 'neu_z']]
                        for i in range(len(messages))], dtype=torch.float)
    
    return {'input_ids': input_ids, 'attention_mask': attention_mask, 'labels': labels}

def to_one_hot(value, num_classes):
    one_hot = np.zeros(num_classes, dtype=int)
    one_hot[value] = 1
    return one_hot.tolist()

def preprocess_function_with_tokenizer_one_hot(examples, tokenizer, num_labels=3):
    messages = examples['message']
    
    tokenized_messages = tokenizer(messages, truncation=True, padding='max_length', max_length=512)
    
    input_ids = tokenized_messages['input_ids']
    attention_mask = tokenized_messages['attention_mask']
    
    labels = torch.tensor([[to_one_hot(examples[col + "_label"][i], num_labels) for col in ['ope_z', 'con_z', 'ext_z', 'agr_z', 'neu_z']]
                        for i in range(len(messages))], dtype=torch.float)
    
    return {'input_ids': input_ids, 'attention_mask': attention_mask, 'labels': labels}