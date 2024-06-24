import torch
from transformers import RobertaTokenizer, RobertaConfig, TrainingArguments, Trainer
from modeling_roberta import RobertaForSequenceClassification
from datasets import Dataset, load_from_disk
import pandas as pd
import numpy as np
import ast
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
import json
import csv
from tqdm import tqdm
from logging_config import setup_logging

# Set up logging configuration
setup_logging(mode='eval')

import logging

# Initialize the logger
logger = logging.getLogger(__name__)

logger.info("Logging setup complete.")

tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
model_path = '/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/tmp_mse_1e-5/checkpoint-1500/'
model = RobertaForSequenceClassification.from_pretrained(model_path, num_labels=1, cache_dir="/data/user_data/jiaruil5/.cache")
model.eval()

def map_to_label(logit):
    labels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    return str(min(labels, key=lambda x: abs(x - logit)))

map_to_label_func = np.vectorize(map_to_label)

test_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data_mse/test_psychgen').select(range(50))

def compute_metrics(pred):
    
    labels = map_to_label_func(np.array(pred.label_ids))
    preds = np.vstack([i.transpose() for i in pred.predictions]).transpose()
    preds = map_to_label_func(preds)
    print(labels)
    print(preds)
    
    label_names = ['O', 'C', 'E', 'A', 'N']
    info = {}
    for dim in range(len(label_names)):
        labels_cur = labels[:, dim]
        preds_cur = preds[:, dim]
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
    report_to="wandb",
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