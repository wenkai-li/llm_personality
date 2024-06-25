import json
import pandas as pd
from tqdm import tqdm
from llm import call
from utils import *
from config import get_model_config
import argparse
import rich 
import random


def llm_config_func(llm):
    llm.temperature = 0
    llm.max_tokens = 4096
    return llm


def get_prediction_list(model, testset, config):
    prediction = []
    with open(testset) as f:
        testset = json.load(f)

    # Subsample testset here
    # num_samples = 200
    # sub_testset = testset[:num_samples]

    post_tokens = [i["input"] for i in testset]

    for tokens in tqdm(post_tokens):
        predict_dict = {}
        prompt = [
        f"Help me complete the sentence with certain Big Five Personality: Openness - median, Conscientiousness - high, Extraversion - median, Agreeableness - high, Neuroticism - low. {tokens}"]
        res = call(
            prompt,
            llm_config_func,
            has_system_prompt=True,
            model_version=model,
            verbose=True,
            **config
        )
        predict_dict['input'] = tokens
        predict_dict['prediction'] = res
        prediction.append(predict_dict)
    return prediction

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--model_name", default=None, type=str, required=True, help = "Choose the evlauate model, the name can be seen in config")
    parser.add_argument("--testset", default="testset/alpaca_big_five_dataset_test.json", type=str, required=False, help="Give a absolute path for testset")
    parser.add_argument("--output_file", default=None, type=str, required=True, help="The output file path and name")
    args = parser.parse_args()

    config = get_model_config(args.model_name)
    predictions = get_prediction_list(args.model_name, args.testset, config)
    
    with open(args.output_file, 'w') as f:
        json.dump(predictions, f, indent=4)

if __name__ == "__main__":
    main()

        

