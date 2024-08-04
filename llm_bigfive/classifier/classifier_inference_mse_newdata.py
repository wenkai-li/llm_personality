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
model_path = '/compute/inst-0-35/jiaruil5/personality/classifier/mse_1e-5/checkpoint-119000/'
model = RobertaForSequenceClassification.from_pretrained(model_path, num_labels=1, cache_dir="/data/user_data/wenkail/.cache")
model.eval()

def map_to_label(logit):
    labels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    return str(min(labels, key=lambda x: abs(x - logit)))

map_to_label_func = np.vectorize(map_to_label)

def map_to_3_label(original_label):
    labels = [0, 1, 2]
    original_label = float(original_label)
    if original_label < 0.3:
        return 0
    elif original_label < 0.7:
        return 1
    else:
        return 2

map_to_3_label_func = np.vectorize(map_to_3_label)

out_f = open('/home/wenkail/llm_personality/llm_bigfive/classifier/results/messages.json', 'w')


from utils import preprocess_function_with_tokenizer_without_labels
# df = pd.read_csv('filtered_big5_data_6_label.csv').sample(n=50, random_state=42)
df = pd.read_csv("./results/messages.csv")
dataset = Dataset.from_pandas(df)
tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
test_dataset = dataset.map(lambda examples: preprocess_function_with_tokenizer_without_labels(examples, tokenizer), batched=True)

def convert_pred(pred):
    print(pred.predictions)
    preds = np.vstack([i.transpose() for i in pred.predictions[1]]).transpose()
    preds = map_to_label_func(preds)
    # print(preds)

    preds = map_to_3_label_func(preds).transpose()
    
    json.dump({
        "preds": preds.tolist()
    }, out_f)

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
    args=training_args
)

predictions = trainer.predict(test_dataset)
convert_pred(predictions)