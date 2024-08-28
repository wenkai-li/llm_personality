import json
import sys
import pandas as pd
import random
import pdb
from tqdm import tqdm

def generate_alpaca_dataset(df, n_words, trait):
    personality_map = {0: "low", 1: "high"}
    traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
    
    dataset = []
    
    for _, row in tqdm(df.iterrows()):
        message = row['message']
        words = message.split()
        
        if len(words) <= n_words:
            continue
        
        input_text = " ".join(words[:n_words])
        output_text = " ".join(words[n_words:])
        
        personality = [f"{trait.capitalize()} - {personality_map[row[f'{trait[0:3]}_z_label']]}"] 
                    #    for trait in traits]
        
        # instruction = "Help me complete the sentence with certain Big Five Personality: {}, {}, {}, {}, {}".format(*personality)
        instruction = "Help me complete the sentence with certain Big Five Personality: {}".format(*personality)
        
        item = {
            "instruction": instruction,
            "input": input_text,
            "output": output_text
        }
        
        dataset.append(item)
    
    return dataset

def main():
    # data = pd.read_csv('/data/user_data/wenkail/llm_personality/data/big5_data_generator_test.csv')
    traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
    # big5_trait = {}
    # for trait in tqdm(traits):
    #     big5_trait[f'{trait}'] = generate_alpaca_dataset(data, 5, trait)
    # # pdb.set_trace()

    # for trait in tqdm(traits):
    #     with open(f"/data/user_data/wenkail/llm_personaliaty/generator/data/generator_test_{trait[0]}.json", "w") as f:
    #         json.dump(big5_trait[f'{trait}'], f, indent = 4)

    for trait in tqdm(traits):
        train = pd.read_csv(f'/data/user_data/wenkail/llm_personality/data/big5_data_generator_{trait[0]}_test.csv')
        test = pd.read_csv(f'/data/user_data/wenkail/llm_personality/data/big5_data_generator_{trait[0]}_test.csv')
        alpaca_train = generate_alpaca_dataset(train, 5, trait)
        alpaca_test = generate_alpaca_dataset(test, 5, trait)

        with open(f"/data/user_data/wenkail/llm_personality/generator/data/generator_train_3_divide_{trait[0]}.json", "w") as f:
            json.dump(alpaca_train, f, indent = 4)

        with open(f"/data/user_data/wenkail/llm_personality/generator/data/generator_test_3_divide_{trait[0]}.json", "w") as f:
            json.dump(alpaca_test, f, indent = 4)

if __name__ == "__main__":
    main()