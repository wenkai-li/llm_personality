import pandas as pd
from datasets import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
import torch

df = pd.read_csv('big5_training_data_with_token.csv')

def preprocess_function(examples):
    tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
    model_inputs = tokenizer(examples['text'], max_length=512, truncation=True, padding="max_length")
    
    labels = torch.tensor([list(map(int, [examples[col][i] for col in ['ope_z', 'con_z', 'ext_z', 'agr_z', 'neu_z']]))
                           for i in range(len(examples['text']))])
    model_inputs['labels'] = labels
    
    return model_inputs

dataset = Dataset.from_pandas(df)
dataset = dataset.map(preprocess_function, batched=True)
train_dataset = dataset.train_test_split(test_size=0.1)["train"]
val_dataset = dataset.train_test_split(test_size=0.1)["test"]

model = RobertaForSequenceClassification.from_pretrained("roberta-large", num_labels=5)

training_args = TrainingArguments(
    output_dir="/data/user_data/wenkail/llm_personality/classifier/roberta/checkpoint",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=30,
    weight_decay=0.01
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

model.save_pretrained('/data/user_data/wenkail/llm_personality/classifier/roberta/model')

tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
inputs = tokenizer("Predict personality scores: Example input text here", return_tensors="pt")
outputs = model(**inputs)
predictions = torch.sigmoid(outputs.logits).detach().numpy()
print(predictions)
