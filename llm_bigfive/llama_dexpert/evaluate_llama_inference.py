import json
import pandas as pd
from tqdm import tqdm
from llm import call
from utils import *
from config import get_model_config
import argparse
import rich 
import random
import pdb

def llm_config_func(llm):
    llm.temperature = 0
    llm.max_tokens = 512
    return llm

def get_prediction_and_write(model, testset, config, output_file):
    with open(testset) as f:
        testset = json.load(f)

    try:
        with open(output_file, 'r') as f:
            processed_count = sum(1 for line in f if line.strip())
            
    except FileNotFoundError:
        processed_count = 0

    for test in tqdm(testset[processed_count:], initial=processed_count, total=len(testset)):
        predict_dict = {}
        prompt = [
        f"{test['instruction']}\n{test['input']}"]
        res = call(
            prompt,
            llm_config_func,
            has_system_prompt=True,
            model_version=model,
            verbose=True,
            **config
        )
        predict_dict['instruction'] = test['instruction']
        predict_dict['input'] = test['input']
        predict_dict['output'] = res
        
        with open(output_file, 'a') as f:
            json.dump(predict_dict, f, indent=4)
            f.write('\n') 

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--model_name", default=None, type=str, required=True, help="Choose the evaluate model, the name can be seen in config")
    parser.add_argument("--testset", default="/data/user_data/wenkail/llm_personality/generator/data/alpaca_big_five_dataset_test_5_tokens.json", type=str, required=False, help="Give an absolute path for testset")
    parser.add_argument("--output_file", default=None, type=str, required=True, help="The output file path and name")
    args = parser.parse_args()

    config = get_model_config(args.model_name)

    get_prediction_and_write(args.model_name, args.testset, config, args.output_file)

if __name__ == "__main__":
    main()