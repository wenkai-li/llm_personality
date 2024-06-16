import torch
from transformers import RobertaTokenizer, RobertaConfig, RobertaForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
import ast
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import json
import csv
from tqdm import tqdm

tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
model_path = '/data/user_data/wenkail/llm_personality/classifier/roberta/model'
model = RobertaForSequenceClassification.from_pretrained(model_path)

def map_to_label(logit):
    labels = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    return min(labels, key=lambda x: abs(x - logit))

df = pd.read_csv('big5_training_data_with_token_roberta.csv')
df = df.sample(frac=0.0001, random_state=42)

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

dataset = Dataset.from_pandas(df.dropna())
dataset = dataset.map(preprocess_function, batched=True)


def test_model(dataset, output_format='csv', output_path='predictions.csv'):
    predictions = []
    true_labels = []

    for example in tqdm(dataset):
        inputs = {'input_ids': torch.tensor(example['input_ids']).unsqueeze(0)}
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            prediction = [map_to_label(logit.item()) for logit in logits[0]]
            predictions.append(prediction)
            true_labels.append(example['labels'])

    if output_format == 'csv':
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['True Labels', 'Predictions'])
            for true_label, prediction in zip(true_labels, predictions):
                writer.writerow([true_label.numpy(), prediction])
    elif output_format == 'json':
        data = {'true_labels': [label for label in true_labels],
                'predictions': [pred for pred in predictions]}
        with open(output_path, 'w') as jsonfile:
            json.dump(data, jsonfile)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

test_model(dataset, output_format='json', output_path='predictions.json')



test_model(dataset, output_format='json', output_path='predictions.json')