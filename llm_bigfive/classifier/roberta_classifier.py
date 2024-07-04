import torch
from transformers import RobertaTokenizer, RobertaConfig, TrainingArguments, Trainer
from modeling_roberta import RobertaForSequenceClassification
from datasets import Dataset
import pandas as pd
import ast
from logging_config import setup_logging
import wandb
# Set up logging configuration
setup_logging()

import logging

# Initialize the logger
logger = logging.getLogger(__name__)

logger.info("Logging setup complete.")

###########
## Save each dataset to a separate directory
# from utils import preprocess_function, preprocess_function_with_tokenizer
# df = pd.read_csv('filtered_big5_data_3_label.csv')
# # # df = df.sample(frac=0.01, random_state=42)
# tokenizer = RobertaTokenizer.from_pretrained('roberta-large')
# dataset = Dataset.from_pandas(df)
# dataset = dataset.map(lambda examples: preprocess_function_with_tokenizer(examples, tokenizer), batched=True)
# train_dataset, val_dataset = dataset.train_test_split(test_size=0.1, seed=42).values()
# val_dataset, test_dataset = val_dataset.train_test_split(test_size=0.4, seed=42).values()
# train_dataset.save_to_disk('/data/user_data/wenkail/llm_personality/data/train_psychgen')
# val_dataset.save_to_disk('/data/user_data/wenkail/llm_personality/data/val_psychgen')
# test_dataset.save_to_disk('/data/user_data/wenkail/llm_personality/data/test_psychgen')

###########
# Load the datasets from the saved directories
from datasets import load_from_disk
train_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data/train_psychgen')
val_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data/val_psychgen')
test_dataset = load_from_disk('/data/user_data/wenkail/llm_personality/data/test_psychgen')

wandb.init(project="llm_personality", name="roberta_finetuning_e3")
num_labels = 1 # we have already defined the sub-loss for each personality dimension in modeling_roberta.py
model = RobertaForSequenceClassification.from_pretrained("roberta-large", num_labels=num_labels, cache_dir="/data/user_data/wenkail/.cache")

training_args = TrainingArguments(
    # output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/test/",
    output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/lwk/e3/checkpoint/",
    evaluation_strategy="steps",
    eval_steps=500,
    learning_rate=1e-3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    save_total_limit=5,                     # Only save the last 5 checkpoints
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
# [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
# (p'(O), y_O), (p'(C), y_C), (p'(E), y_E), (p'(A), y_A), (p'(N), y_N)