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
from sklearn.metrics import classification_report

# Set up logging configuration
setup_logging(mode='eval')

import logging

# Initialize the logger
logger = logging.getLogger(__name__)

logger.info("Logging setup complete.")

tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
model_path = '/compute/inst-0-35/jiaruil5/personality/classifier/mse_1e-5/checkpoint-119000/'
model = RobertaForSequenceClassification.from_pretrained(model_path, num_labels=1, cache_dir="/data/user_data/jiaruil5/.cache")
model.eval()

def get_json_list(path):
    import json
    f = open(path, 'r')
    info = []
    for line in f.readlines():
        info.append(json.loads(line))
    return info

def map_to_label(logit):
    labels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    return str(min(labels, key=lambda x: abs(x - logit)))

map_to_label_func = np.vectorize(map_to_label)

def map_to_3_label(original_label):
    original_label = float(original_label)
    if original_label < 0.3:
        return 2 # low, different from the original label
    elif original_label < 0.7:
        return 1
    else:
        return 0 # high, different from the original label

map_to_3_label_func = np.vectorize(map_to_3_label)

out_f = open('/home/jiaruil5/personality/llm_personality/llm_bigfive/classifier/results/dexpert_gen_data_test.json', 'w')


from utils import preprocess_function_with_tokenizer_without_labels

in_dir = "/data/user_data/wenkail/llm_personality/profiles/"
data = []
# for file in ['env_profiles_1.jsonl', 'env_profiles_2.jsonl', 'env_profiles_3.jsonl', 'env_profiles_4.jsonl', 'env_profiles_5.jsonl']:
for file in ['env_profiles_1.jsonl', 'env_profiles_2.jsonl', 'env_profiles_3.jsonl']:
    file_path = in_dir + file
    data.extend(get_json_list(file_path))
df = pd.DataFrame().from_records(data)
df_personality = df['personality'].str.split(" ", expand=True)
df_personality.columns = ['bf_o', 'bf_c', 'bf_e', 'bf_a', 'bf_n']
df = pd.concat([df, df_personality], axis=1)
df.rename(columns={'response': 'message'}, inplace=True)

dataset = Dataset.from_pandas(df.dropna())
tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
test_dataset = dataset.map(lambda examples: preprocess_function_with_tokenizer_without_labels(examples, tokenizer), batched=True)

def convert_pred(pred):
    print(pred.predictions)
    preds = np.vstack([i.transpose() for i in pred.predictions[1]]).transpose()
    preds = map_to_label_func(preds)
    # print(preds)

    preds = map_to_3_label_func(preds).transpose()
    return preds
    # json.dump({
    #     "preds": preds.tolist()
    # }, out_f)

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
preds = convert_pred(predictions).tolist() # a list of list, each inner list is for one personality trait
ground_truth = df[['bf_o', 'bf_c', 'bf_e', 'bf_a', 'bf_n']].applymap(lambda x: int(x)).values.transpose().tolist()

json.dump({
    "pred": preds,
    "label": ground_truth
}, out_f)

for idx, dim in enumerate(['Openness', 'Conscientiousness', 'Extraversion', 'Agreeablenes', 'Neuroticism']):
    print(dim)
    print(classification_report(ground_truth[idx], preds[idx], digits=4))