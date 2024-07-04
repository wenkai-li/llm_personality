import pandas as pd
from transformers import RobertaTokenizer
from tqdm import tqdm

# Initialize the tqdm progress bar for pandas apply
tqdm.pandas()

# Load your DataFrame
data = pd.read_csv("big5_training_data_degree.csv")

# Initialize the tokenizer
tokenizer = RobertaTokenizer.from_pretrained("roberta-large")

# Tokenize the 'message' column with a progress bar
data['message_tokens'] = data['message'].progress_apply(lambda x: tokenizer.encode(x, add_special_tokens=True))

# Save the DataFrame to a new CSV file
data.to_csv("big5_training_data_with_token_roberta.csv", index=False)
