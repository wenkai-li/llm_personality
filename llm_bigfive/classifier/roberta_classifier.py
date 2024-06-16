import torch
from transformers import RobertaTokenizer, RobertaConfig, TrainingArguments, Trainer
from modeling_roberta import RobertaForSequenceClassification
from datasets import Dataset
import pandas as pd
import ast
from logging_config import setup_logging

# Set up logging configuration
setup_logging()

import logging

# Initialize the logger
logger = logging.getLogger(__name__)

logger.info("Logging setup complete.")

###########
# Save each dataset to a separate directory
# df = pd.read_csv('big5_training_data_with_token_roberta.csv')
# # df = df.sample(frac=0.01, random_state=42)

# def preprocess_function(examples):
#     if isinstance(examples['message_tokens'][0], str):
#         input_ids = [ast.literal_eval(tokens) for tokens in examples['message_tokens']]
#     else:
#         input_ids = examples['message_tokens']
    
#     max_length = 512
#     input_ids = [tokens[:max_length] + [0] * (max_length - len(tokens)) for tokens in input_ids]

#     labels = torch.tensor([[examples[col + "_level"][i] for col in ['ope_z', 'con_z', 'ext_z', 'agr_z', 'neu_z']]
#                            for i in range(len(examples['message_tokens']))], dtype=torch.float)
    
#     return {'input_ids': input_ids, 'labels': labels}

# dataset = Dataset.from_pandas(df.dropna())
# dataset = dataset.map(preprocess_function, batched=True)
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


num_labels = 1 # we have already defined the sub-loss for each personality dimension in modeling_roberta.py
model = RobertaForSequenceClassification.from_pretrained("roberta-large", num_labels=num_labels, cache_dir="/data/user_data/jiaruil5/.cache")

training_args = TrainingArguments(
    output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/ljr/test/",
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
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

model.save_pretrained('/data/user_data/wenkail/llm_personality/classifier/roberta/model_4')

tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
inputs = tokenizer("Predict personality scores: Example input text here", return_tensors="pt")
outputs = model(**inputs)
predictions = outputs.logits
print(predictions)


# O, C, E, A, N
# [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
# (p'(O), y_O), (p'(C), y_C), (p'(E), y_E), (p'(A), y_A), (p'(N), y_N)