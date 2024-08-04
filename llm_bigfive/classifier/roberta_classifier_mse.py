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
wandb.init(project="llm_personality", entity="kyle_organization", name="test-mse-whole-1e-5")

###########
# ## MSE loss: Save each dataset to a separate directory
# from utils import preprocess_function_with_tokenizer
# for split in ['train', 'val', 'test']:
#     df = pd.read_csv(f'/data/user_data/wenkail/llm_personality/data/big5_data_classifier_{split}.csv')
#     dataset = Dataset.from_pandas(df.dropna())
#     tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
#     dataset = dataset.map(lambda examples: preprocess_function_with_tokenizer(examples, tokenizer), batched=True)
#     dataset.save_to_disk(f'/data/user_data/wenkail/llm_personality/data_mse/{split}_psychgen')
# exit(0)
###########

# Load the datasets from the saved directories
from datasets import load_from_disk
train_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data_mse/train_psychgen')
val_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data_mse/val_psychgen')
test_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data_mse/test_psychgen')

# if using MSE loss, then we should set num_labels to 1; if using Cross Entropy loss, then we should set num_labels to 3
num_labels = 1 # we have already defined the sub-loss for each personality dimension in modeling_roberta.py
model = RobertaForSequenceClassification.from_pretrained("roberta-large", num_labels=num_labels, cache_dir="/data/user_data/jiaruil5/.cache")

training_args = TrainingArguments(
    # output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/test/",
    # output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/tmp_mse_1e-5/",
    output_dir="/compute/babel-0-37/jiaruil5/personality/checkpoints/classifier/mse_1e-5/",
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
    gradient_accumulation_steps=16,
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
# [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
# (p'(O), y_O), (p'(C), y_C), (p'(E), y_E), (p'(A), y_A), (p'(N), y_N)