import torch
from transformers import RobertaTokenizer, RobertaConfig, TrainingArguments, Trainer
from modeling_roberta import RobertaForSequenceClassification
from datasets import Dataset
import pandas as pd
import ast
import numpy as np
from logging_config import setup_logging

# Set up logging configuration
setup_logging()

import logging

# Initialize the logger
logger = logging.getLogger(__name__)

logger.info("Logging setup complete.")

import wandb
wandb.init(project="llm_personality", entity="kyle_organization", name="test-ce-whole-1e-5")

###########
# ## Cross Entropy loss: Save each dataset to a separate directory
# from utils import preprocess_function_with_tokenizer_one_hot
# df = pd.read_csv('filtered_big5_data_3_label.csv')

# dataset = Dataset.from_pandas(df.dropna())
# tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
# dataset = dataset.map(lambda examples: preprocess_function_with_tokenizer_one_hot(examples, tokenizer), batched=True)
# train_dataset, val_dataset = dataset.train_test_split(test_size=0.1, seed=42).values()
# val_dataset, test_dataset = val_dataset.train_test_split(test_size=0.4, seed=42).values()
# train_dataset.save_to_disk('/data/user_data/wenkail/llm_personality/data_ce/train_psychgen')
# val_dataset.save_to_disk('/data/user_data/wenkail/llm_personality/data_ce/val_psychgen')
# test_dataset.save_to_disk('/data/user_data/wenkail/llm_personality/data_ce/test_psychgen')
###########

# Load the datasets from the saved directories
from datasets import load_from_disk
train_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data_ce/train_psychgen')
val_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data_ce/val_psychgen')
test_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data_ce/test_psychgen')

# def convert_labels_to_int(example):
#     labels = np.array(example['labels'])
#     labels = labels.astype(int)
#     example['labels'] = labels.tolist()
#     return example

# # Apply the transformation to convert labels from float to int
# train_dataset = train_dataset.map(convert_labels_to_int)
# val_dataset = val_dataset.map(convert_labels_to_int)
# test_dataset = test_dataset.map(convert_labels_to_int)

# if using MSE loss, then we should set num_labels to 1; if using Cross Entropy loss, then we should set num_labels to 3
num_labels = 3 # we have already defined the sub-loss for each personality dimension in modeling_roberta.py
model = RobertaForSequenceClassification.from_pretrained("roberta-large", num_labels=num_labels, cache_dir="/data/user_data/jiaruil5/.cache")

training_args = TrainingArguments(
    # output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/test/",
    output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/tmp_ce_1e-5/",
    evaluation_strategy="steps",
    eval_steps=500,
    learning_rate=1e-5,
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
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

# O, C, E, A, N
# one hot of [0 Low, Neutral, High]
# (p'(O), y_O), (p'(C), y_C), (p'(E), y_E), (p'(A), y_A), (p'(N), y_N)