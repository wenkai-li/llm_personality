import torch
from transformers import RobertaTokenizer, RobertaConfig, RobertaForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
import ast

df = pd.read_csv('big5_training_data_with_token_roberta.csv')
df = df.sample(frac=0.01, random_state=42)

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
train_dataset, val_dataset = dataset.train_test_split(test_size=0.1).values()

num_labels = 5
model = RobertaForSequenceClassification.from_pretrained("roberta-large", num_labels=num_labels)

training_args = TrainingArguments(
    output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/checkpoint_e4",
    eval_strategy="steps",
    eval_steps=500,
    learning_rate=2e-4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=30,
    weight_decay=0.01,
    save_strategy="steps",
    save_steps=500,
    load_best_model_at_end=True,
    logging_dir='./logs',
    logging_steps=10,
    dataloader_num_workers=4,
    gradient_accumulation_steps=2,
    fp16=True
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
