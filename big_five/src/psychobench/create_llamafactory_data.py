import json
import os

in_dir_path = "questions"
out_dir_path = "questions_llamafactory"

out_info_path = open(os.path.join(out_dir_path, "dataset_info.json"), 'w')
data_info = {}

levels = ['high', 'median', 'low']
for file in os.listdir(in_dir_path):
    file_path = os.path.join(in_dir_path, file)
    data = [json.loads(i) for i in open(file_path, 'r').readlines()]
    
    out_data = []
    for dim in range(5):
        for level in [0, 2]:
            current_levels = ['median', 'median', 'median', 'median', 'median']
            current_levels[dim] = levels[level]
            current_level_idx = "".join([str(levels.index(i)) for i in current_levels])
            name = file.split("70b-")[-1] + "_" + current_level_idx
            
            for item in data:
                info = {
                    "instruction": f"You are a helpful assistant with the following Big Five personality traits: Openness - {current_levels[0]}, Conscientiousness - {current_levels[1]}, Extraversion - {current_levels[2]}, Agreeableness - {current_levels[3]}, Neuroticism - {current_levels[4]}",
                    "input": item[-1]['content'],
                    "output": name
                }
                out_data.append(info)

    
    out_filename = file + ".json"
    out_file_path = os.path.join(out_dir_path, out_filename)
    out_f = open(out_file_path, 'w')
    json.dump(out_data, out_f, indent=2, ensure_ascii=False)
    out_f.flush()

    data_info[file.split("70b-")[-1]] = {
        "file_name": out_filename,
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "response": "output",
        }
    }
    
json.dump(data_info, out_info_path, indent=4, ensure_ascii=False)