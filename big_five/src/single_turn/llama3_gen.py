import json
import sys
from tqdm import tqdm
import numpy as np
np.random.seed(42)

sys.path.append("../")
from dexpert.llama3 import LLAMA3
from prompts import generate_prompt

model = LLAMA3()

def get_response(prompt):
    return model.generate(prompt)

agent_profiles = json.load(open("../data/database/agent_profiles.json", 'r'))['_default']
env_profiles = json.load(open("../data/database/environment_profiles.json", 'r'))['_default']

out_f = open("sample20_11111_11211.jsonl", 'a')
p1_big_five = [1, 1, 1, 1, 1]
p2_big_five = [1, 1, 2, 1, 1]

len_agent, len_env = len(agent_profiles), len(env_profiles)
agent_lst, env_lst = [str(i) for i in np.arange(1, len_agent+1)], [str(i) for i in np.arange(1, len_env+1)]

np.random.shuffle(env_lst)

for idx, env_idx in tqdm(enumerate(env_lst[:20])):
    # env
    env_profile = env_profiles[env_idx]
    
    # agent
    agent1_idx, agent2_idx = np.random.choice(
        agent_lst,
        2,
        replace=False
    )
    agent1_profile = agent_profiles[agent1_idx]
    agent2_profile = agent_profiles[agent2_idx]
    
    # generate prompt for turn 0
    prompt_turn_0 = generate_prompt(
        agent1_profile,
        agent2_profile,
        env_profile,
        p1_personality_and_values=p1_big_five,
        p2_personality_and_values=p2_big_five,
        current_turn_index=0
    )
    
    response_turn_0 = get_response(prompt_turn_0)
    
    # generate prompt for turn 1
    prompt_turn_1 = generate_prompt(
        agent1_profile,
        agent2_profile,
        env_profile,
        p1_personality_and_values=p1_big_five,
        p2_personality_and_values=p2_big_five,
        current_turn_index=1,
        p1_argument = response_turn_0
    )
    
    response_turn_1 = get_response(prompt_turn_1)
    
    result_info = {
        "env_idx": env_idx,
        "agent1_idx": agent1_idx,
        "agent2_idx": agent2_idx,
        "prompt_turn_0": prompt_turn_0,
        "response_turn_0": response_turn_0,
        "prompt_turn_1": prompt_turn_1,
        "response_turn_1": response_turn_1,
    }
    json.dump(result_info, out_f)
    out_f.write("\n")
    out_f.flush()