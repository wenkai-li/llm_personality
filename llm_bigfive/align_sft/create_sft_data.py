import json
import re
import random
from sklearn.model_selection import train_test_split

def get_json_list(path):
    import json
    f = open(path, 'r')
    info = []
    for line in f.readlines():
        info.append(json.loads(line))
    return info

def process_str(in_str):
    return re.sub(r'\*.*?\*|\(.*?\)', '', in_str)

in_dir = "/data/user_data/wenkail/llm_personality/profiles/env_profiles_"
out_file = "/data/user_data/wenkail/llm_personality/align/data_sft/train.json"
out_f = open(out_file, 'w')
out_test_file = out_file.replace("train.json", 'test.json')
out_test_f = open(out_test_file, 'w')

data_dict = {}
for trait in ['o', 'c', 'e', 'a', 'n']:
    data_dict[trait] = []
    
    for file in ['_1.jsonl', '_2.jsonl']:
        file_path = in_dir + trait + file
        data_dict[trait].extend(get_json_list(file_path))

json_lst = []
for idx in range(0, len(data_dict['o']), 3):
    for trait in ['o', 'c', 'e', 'a', 'n']:
        data = data_dict[trait]
        assert data[idx]['turn'] == 0
        
        personx = process_str(data[idx]['response'])
        for i in range(idx+1,idx+3):
            info = {}
            persony = process_str(data[i]['response'])
            bfi_traits = [int(trait) for trait in data[i]['personality'].split(" ")]
            levels = ['high', 'low']
            
            trait_str = ""
            if trait == 'o':
                trait_str = f"Openness - {levels[bfi_traits[0]]}"
            elif trait == 'c':
                trait_str = f"Conscientiousness - {levels[bfi_traits[1]]}"
            elif trait == 'e':
                trait_str = f"Extraversion - {levels[bfi_traits[2]]}"
            elif trait == 'a':
                trait_str = f"Agreeableness - {levels[bfi_traits[3]]}"
            elif trait == 'n':
                trait_str = f"Neuroticism - {levels[bfi_traits[4]]}"
            
            instruction = f"You are a helpful assistant with the following Big Five personality traits: {trait_str}"
            info['instruction'] = instruction
            info['input'] = personx
            info['output'] = persony
            json_lst.append(info)

print(len(json_lst))
train_data, test_data = train_test_split(json_lst, test_size=0.1, shuffle=False)
random.shuffle(train_data)
random.shuffle(test_data)

json.dump(train_data, out_f, indent=2, ensure_ascii=False)
out_f.flush()

json.dump(test_data, out_test_f, indent=2, ensure_ascii=False)
out_test_f.flush()

