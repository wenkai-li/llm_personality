import json
import sys
from tqdm import tqdm
import numpy as np
np.random.seed(42)

sys.path.append("../")
from dexpert.llama3 import LLAMA3

model = LLAMA3()

out_f = open("goal_nli.jsonl", 'a')

def get_response(prompt):
    return model.generate(prompt)

env_profiles = json.load(open("../data/database/environment_profiles.json", 'r'))['_default']
len_env = len(env_profiles)
env_lst = [str(i) for i in np.arange(1, len_env+1)]

for idx, env_idx in tqdm(enumerate(env_lst)):
    env_profile = env_profiles[env_idx]
    
    prompt = """Is the first social goal below entailed, contradicted, or unaffected by the second social goal? Directly answer "Entailment", or "Contradictory", or "Neutral" without any explanations.

The first goal: {goal1}
The second goal: {goal2}""".format(
        goal1 = env_profile['agent_goals'][0],
        goal2 = env_profile['agent_goals'][1],
    )
    response = get_response(prompt)
    out_f.write(response)
    out_f.write("\n")
    out_f.flush()