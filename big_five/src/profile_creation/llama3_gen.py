import json
import sys
from tqdm import tqdm
import numpy as np
import pandas as pd
import argparse
import re
np.random.seed(42)

from prompts import generate_prompt
sys.path.append("../dexpert/")
from dexpert import DExpertGenerator

def remove_double_quotes(s):
    # Remove double quotes from the beginning and end
    return re.sub(r'^"+|"+$', '', s)


class CO3Sotopia():
    def __init__(self, args):
        self.args = args
        
        class Args:
            model_id = "meta-llama/Meta-Llama-3-70B-Instruct"
            cache_dir = "/compute/babel-1-31/jiaruil5/.cache/"

        class ArgsExpert:
            model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
            cache_dir = "/data/user_data/jiaruil5/.cache/"

        self.model = DExpertGenerator(args=Args, args_expert=ArgsExpert)
        self.data = pd.read_csv(args.in_file).to_dict(orient='records')
    
    def process_response(self, response):
        try:
            # split by \n\n and get the middle one?
            if ":\n\n" in response:
                response = response.split(":\n\n")
                response = response[-1]
            # remove quotation marks at the beginning and the end
            response = remove_double_quotes(response)
            return response
        except Exception as e:
            print("Error during processing response", response)
            return response
        
    def generate_messages(self, prompt):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        return messages
    
    def generate_expert_messages(self, big_five_level):
        level_lst = ['high', 'median', 'low']
        prompt = f"Help me complete the sentence with certain Big Five Personality: Openness - {level_lst[big_five_level[0]]}, Conscientiousness - {level_lst[big_five_level[1]]}, Extraversion - {level_lst[big_five_level[2]]}, Agreeableness - {level_lst[big_five_level[3]]}, Neuroticism - {level_lst[big_five_level[4]]}\n"
        messages = [
            {"role": "user", "content": prompt}
        ]
        return messages
        
    def generate_dialogue(self, idx, env_info, p1_big_five, p2_big_five, out_f):
        # generate prompt for turn 0
        prompt_turn_0 = generate_prompt(
            env_info,
            # p1_personality_and_values=p1_big_five,
            # p2_personality_and_values=p2_big_five,
            current_turn_index=0
        )
        
        response_turn_0 = self.process_response(self.model.generate(
            messages = self.generate_messages(prompt_turn_0),
            messages_expert = self.generate_expert_messages(p1_big_five),
            alpha = self.args.alpha,
        ))
        
        # generate prompt for turn 1
        prompt_turn_1 = generate_prompt(
            env_info,
            # p1_personality_and_values=p1_big_five,
            # p2_personality_and_values=p2_big_five,
            current_turn_index=1,
            p1_argument = response_turn_0
        )
        
        response_turn_1 = self.process_response(self.model.generate(
            messages = self.generate_messages(prompt_turn_1),
            messages_expert = self.generate_expert_messages(p2_big_five),
            alpha = self.args.alpha,
        ))
        
        result_info = {
            "env_idx": idx,
            "env_info": env_info,
            "personality_0": " ".join(map(str, p1_big_five)),
            "prompt_turn_0": prompt_turn_0,
            "response_turn_0": response_turn_0,
            "personality_1": " ".join(map(str, p2_big_five)),
            "prompt_turn_1": prompt_turn_1,
            "response_turn_1": response_turn_1,
        }
        json.dump(result_info, out_f)
        out_f.write("\n")
        out_f.flush()
    
    def run(self):
        out_f = open(self.args.out_file, 'a')
        p2_big_five_ref = [1, 1, 1, 1, 1]
        for idx, env_info in tqdm(enumerate(self.data)):            
            p1_big_five = list(np.random.choice(3, 5, replace=True))
            for dim in [0, 1, 2, 3, 4]:
                for level in [0, 1, 2]:
                    p2_big_five = p2_big_five_ref.copy()
                    p2_big_five[dim] = level
                    self.generate_dialogue(idx, env_info, p1_big_five, p2_big_five, out_f)
            
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arguments for generating dialogues')
    parser.add_argument("--in_file", type=str, default="/data/user_data/wenkail/llm_personality/soda_data/sample_10000.csv", help="The file of the sampled soda training data")
    parser.add_argument("--out_file", type=str, default="/data/user_data/wenkail/llm_personality/profiles/env_profiles.jsonl")
    parser.add_argument("--alpha", type=float, default=1.0)
    args = parser.parse_args()
    soda_maker = CO3Sotopia(args)
    soda_maker.run()