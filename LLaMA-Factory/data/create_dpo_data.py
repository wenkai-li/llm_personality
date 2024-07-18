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
out_file = "/data/user_data/wenkail/llm_personality/align/data_dpo/train.json"
out_f = open(out_file, 'w')
out_test_file = out_file.replace("train.json", 'test.json')
out_test_f = open(out_test_file, 'w')

data = []
for file in ['1.jsonl', '2.jsonl', '3.jsonl', '4.jsonl', '5.jsonl']:
    file_path = in_dir + file
    data.extend(get_json_list(file_path))
print(len(data))
json_lst = []
for idx in range(0, len(data), 12):
    assert data[idx]['turn'] == 0
    
    personx = process_str(data[idx]['response'])
    
    levels = ['high', 'median', 'low']
    # 1, (0, 2), 0 and 2 are randomly sampled from the five dimensions
    info_1 = {}
    info_1['conversations'] = [{
        "from": "human",
        "value": f"You are a helpful assistant with the following Big Five personality traits: Openness - {levels[1]}, Conscientiousness - {levels[1]}, Extraversion - {levels[1]}, Agreeableness - {levels[1]}, Neuroticism - {levels[1]}\n{personx}"
    }]
    rand_dim = random.choice([0, 1, 2, 3, 4])
    info_1['chosen'] = {
        "from": "gpt",
        "value": process_str(data[idx + 1]['response'])
    }
    info_1['rejected_1'] = {
        "from": "gpt",
        "value": process_str(data[idx + 2 + rand_dim*2]['response'])
    }
    info_1['rejected_2'] = {
        "from": "gpt",
        "value": process_str(data[idx + 2 + rand_dim*2 + 1]['response'])
    }
    json_lst.append(info_1)
    
    for i in range(idx+2, idx+12, 2):
        # 0, (1, 2) x 5
        info_2 = {}
        bfi_traits = [int(trait) for trait in data[i]['personality'].split(" ")]
        info_2['conversations'] = [{
            "from": "human",
            "value": f"You are a helpful assistant with the following Big Five personality traits: Openness - {levels[bfi_traits[0]]}, Conscientiousness - {levels[bfi_traits[1]]}, Extraversion - {levels[bfi_traits[2]]}, Agreeableness - {levels[bfi_traits[3]]}, Neuroticism - {levels[bfi_traits[4]]}\n{personx}"
        }]
        info_2['chosen'] = {
            "from": "gpt",
            "value": process_str(data[i]['response'])
        }
        info_2['rejected_1'] = {
            "from": "gpt",
            "value": process_str(data[idx+1]['response'])
        }
        info_2['rejected_2'] = {
            "from": "gpt",
            "value": process_str(data[i+1]['response'])
        }
        json_lst.append(info_2)
        
        # 2, (0, 1) x 5
        info_3 = {}
        bfi_traits = [int(trait) for trait in data[i+1]['personality'].split(" ")]
        info_3['conversations'] = [{
            "from": "human",
            "value": f"You are a helpful assistant with the following Big Five personality traits: Openness - {levels[bfi_traits[0]]}, Conscientiousness - {levels[bfi_traits[1]]}, Extraversion - {levels[bfi_traits[2]]}, Agreeableness - {levels[bfi_traits[3]]}, Neuroticism - {levels[bfi_traits[4]]}\n{personx}"
        }]
        info_3['chosen'] = {
            "from": "gpt",
            "value": process_str(data[i+1]['response'])
        }
        info_3['rejected_1'] = {
            "from": "gpt",
            "value": process_str(data[idx+1]['response'])
        }
        info_3['rejected_2'] = {
            "from": "gpt",
            "value": process_str(data[i]['response'])
        }
        json_lst.append(info_3)

print(len(json_lst))
train_data, test_data = train_test_split(json_lst, test_size=0.1, shuffle=False)
random.shuffle(train_data)
random.shuffle(test_data)

json.dump(train_data, out_f, indent=2, ensure_ascii=False)
out_f.flush()

json.dump(test_data, out_test_f, indent=2, ensure_ascii=False)
out_test_f.flush()

