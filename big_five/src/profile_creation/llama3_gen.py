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
            # model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
            # cache_dir = "/data/user_data/jiaruil5/.cache/"
            model_id = "/compute/babel-0-37/jiaruil5/personality/checkpoints/generator_whole_1e-6/checkpoint-9000/"
            cache_dir = None

        self.model = DExpertGenerator(args=Args, args_expert=ArgsExpert)
        self.data = pd.read_csv(args.in_file).to_dict(orient='records')
        curr_idx, total_idx = args.chunk.split("/")
        curr_idx = int(curr_idx)
        total_idx = int(total_idx)
        parts = len(self.data) // total_idx
        self.data = self.data[(curr_idx-1)*parts:curr_idx*parts]
        
    
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
    
    def generate_dialogue_turn0(self, idx, env_info, p1_big_five, out_f):
        # generate prompt for turn 0
        self.prompt_turn_0 = generate_prompt(
            env_info,
            current_turn_index=0,
            p1_personality_and_values=p1_big_five,
            # p2_personality_and_values=p2_big_five,
        )
        
        self.response_turn_0 = self.process_response(self.model.generate(
            messages = self.generate_messages(self.prompt_turn_0),
            messages_expert = self.generate_expert_messages(p1_big_five),
            alpha = self.args.alpha,
        ))
        
        result_info = {
            "env_idx": idx,
            "env_info": env_info,
            "personality": " ".join(map(str, p1_big_five)),
            "turn": 0,
            "prompt": self.prompt_turn_0,
            "response": self.response_turn_0,
        }
        json.dump(result_info, out_f)
        out_f.write("\n")
        out_f.flush()
    
    def generate_dialogue_turn1(self, idx, env_info, p2_big_five, out_f):
        
        
        # generate prompt for turn 1
        prompt_turn_1 = generate_prompt(
            env_info,
            current_turn_index=1,
            # p1_personality_and_values=p1_big_five,
            p2_personality_and_values=p2_big_five,
            p1_argument = self.response_turn_0,
        )
        
        response_turn_1 = self.process_response(self.model.generate(
            messages = self.generate_messages(prompt_turn_1),
            messages_expert = self.generate_expert_messages(p2_big_five),
            alpha = self.args.alpha,
        ))
        
        result_info = {
            "env_idx": idx,
            "env_info": env_info,
            "personality": " ".join(map(str, p2_big_five)),
            "turn": 1,
            "prompt": prompt_turn_1,
            "response": response_turn_1,
        }
        json.dump(result_info, out_f)
        out_f.write("\n")
        out_f.flush()
    
    def run(self):
        out_f = open(self.args.out_file, 'a')
        p2_big_five_ref = [1, 1, 1, 1, 1]
        for idx, env_info in tqdm(enumerate(self.data)):            
            p1_big_five = list(np.random.choice(3, 5, replace=True))
            self.generate_dialogue_turn0(idx, env_info, p1_big_five, out_f)
            self.generate_dialogue_turn1(idx, env_info, p2_big_five_ref, out_f)
            for dim in [0, 1, 2, 3, 4]:
                for level in [0, 2]:
                    p2_big_five = p2_big_five_ref.copy()
                    p2_big_five[dim] = level
                    self.generate_dialogue_turn1(idx, env_info, p2_big_five, out_f)
            
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arguments for generating dialogues')
    parser.add_argument("--in_file", type=str, default="/data/user_data/wenkail/llm_personality/soda_data/sample_10000.csv", help="The file of the sampled soda training data")
    parser.add_argument("--out_file", type=str, default="/data/user_data/wenkail/llm_personality/profiles/env_profiles_new.jsonl")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--chunk", type=str, default="1/5")
    args = parser.parse_args()
    soda_maker = CO3Sotopia(args)
    soda_maker.run()