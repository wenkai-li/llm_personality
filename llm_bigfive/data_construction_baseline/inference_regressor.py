import torch
from transformers import RobertaTokenizer, RobertaConfig, TrainingArguments, Trainer
from modeling_roberta import RobertaForSequenceClassification
from datasets import Dataset, load_from_disk
import pandas as pd
import numpy as np
import ast
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score, mean_absolute_error, mean_squared_error, r2_score
import json
import csv
from tqdm import tqdm
from logging_config import setup_logging
import sys

# Set up logging configuration
setup_logging(mode='eval')

trait_trait = sys.argv[1]

import logging

# Initialize the logger
logger = logging.getLogger(__name__)

logger.info("Logging setup complete.")

tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
model_path = '/data/user_data/wenkail/llm_personality/classifier/mse_1e-5/checkpoint-3500/'
model = RobertaForSequenceClassification.from_pretrained(model_path, num_labels=1, cache_dir="/data/user_data/jiaruil5/.cache")
model.eval()

out_f = open(f'/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/direct/classifier_data_{trait_trait}.json', 'w')

## first run
# import torch

# def preprocess_function_with_tokenizer(examples, tokenizer):
#     messages = examples['message']
    
#     tokenized_messages = tokenizer(messages, truncation=True, padding='max_length', max_length=512)
    
#     input_ids = tokenized_messages['input_ids']
#     attention_mask = tokenized_messages['attention_mask']
    
#     labels = torch.tensor([[examples[col + "_label"][i] for col in ['ope_z', 'con_z', 'ext_z', 'agr_z', 'neu_z']]
#                         for i in range(len(messages))], dtype=torch.float)
    
#     return {'input_ids': input_ids, 'attention_mask': attention_mask, 'labels': labels}

# df_1 = pd.DataFrame().from_records([json.loads(i) for i in open("/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/direct/out_direct.jsonl", 'r').readlines()])
# df_2 = pd.read_json("/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/data_input.json")
# df = pd.DataFrame()
# df['message'] = df_1['post']
# labels = [[],[],[],[],[]]
# for idx, row in df_2.iterrows():
#     traits = ['o', 'c', 'e', 'a', 'n']
#     true_i = None
#     for i, trait in enumerate(traits):
#         if row['trait'] == trait:
#             true_i = i
#             if row['level'] == 'high':
#                 labels[i].append(1)
#             elif row['level'] == 'low':
#                 labels[i].append(0)
#             break
#     for i in range(5):
#         if i != true_i:
#             labels[i].append(2)
# df['ope_z_label'] = labels[0]
# df['con_z_label'] = labels[1]
# df['ext_z_label'] = labels[2]
# df['agr_z_label'] = labels[3]
# df['neu_z_label'] = labels[4]

# df = np.array_split(df, 5)
# for idx, i in enumerate(['o', 'c', 'e', 'a', 'n']):
#     dataset = Dataset.from_pandas(df[idx].dropna())
#     tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
#     dataset = dataset.map(lambda examples: preprocess_function_with_tokenizer(examples, tokenizer), batched=True)
#     dataset.save_to_disk(f'/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/direct/classifier_data_{i}')
# exit(0)

## second run
test_dataset = load_from_disk(f'/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/direct/classifier_data_{trait_trait}')#.select(range(100))

def map_to_2_label(original_label):
    original_label = float(original_label)
    if original_label < 0.5:
        return 0
    else:
        return 1

map_to_2_label_func = np.vectorize(map_to_2_label)

def compute_metrics(pred):
    
    orig_labels = np.array(pred.label_ids).transpose()
    orig_preds = np.vstack([i.transpose() for i in pred.predictions])
    
    labels = map_to_2_label_func(orig_labels)
    preds = map_to_2_label_func(orig_preds)
    
    json.dump({
        "orig_labels": orig_labels.tolist(),
        "orig_preds": orig_preds.tolist(),
        "labels": labels.tolist(),
        "preds": preds.tolist()
    }, out_f)
    out_f.flush()
    
    label_names = ['O', 'C', 'E', 'A', 'N']
    info = {}
    for dim in range(len(label_names)):
        labels_cur = labels[dim, :]
        preds_cur = preds[dim, :]
        f1 = f1_score(labels_cur, preds_cur, average='weighted')
        accuracy = accuracy_score(labels_cur, preds_cur)
        precision = precision_score(labels_cur, preds_cur, average='weighted')
        recall = recall_score(labels_cur, preds_cur, average='weighted')

        info[f'f1_{label_names[dim]}'] = round(f1, 2)
        info[f'accuracy_{label_names[dim]}'] = round(accuracy, 2)
        info[f'precision_{label_names[dim]}'] = round(precision, 2)
        info[f'recall_{label_names[dim]}'] = round(recall, 2)
        
    return info

training_args = TrainingArguments(
    # output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/test/",
    output_dir="results/",
    evaluation_strategy="steps",
    eval_steps=500,
    learning_rate=1e-4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    save_total_limit=2,                     # Only save the last 2 checkpoints
    load_best_model_at_end=True,            # Load the best model at the end
    metric_for_best_model="eval_loss",      # Metric for determining best model
    greater_is_better=False,
    # report_to="wandb",
    logging_dir='./logs',
    logging_steps=10,
    log_level='info',
    dataloader_num_workers=4,
    gradient_accumulation_steps=2,
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
)

eval_results = trainer.evaluate()

# Print the evaluation results
for key, value in eval_results.items():
    print(f"{key}: {value:.2f}")
    
data = json.load(open(f'/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/direct/classifier_data_{trait_trait}.json', 'r'))
for idx, dim in enumerate(['Openness', 'Conscientiousness', 'Extraversion', 'Agreeablenes', 'Neuroticism']):
    print(dim)
    print("Classification results:")
    print(classification_report(data['labels'][idx], data['preds'][idx], digits=4))
    
    print("Regression results:")
    mae = mean_absolute_error(data['orig_labels'][idx], data['orig_preds'][idx])
    print(f"Mean absolute error: {mae:.4f}")
    mse = mean_squared_error(data['orig_labels'][idx], data['orig_preds'][idx])
    print(f"Root mean squared error: {np.sqrt(mse):.4f}")
    r2 = r2_score(data['orig_labels'][idx], data['orig_preds'][idx])
    print(f"R2: {r2:.4f}")