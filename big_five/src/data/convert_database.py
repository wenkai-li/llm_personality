import json

# in_file = json.load(open("sotopia_data/agent_profiles.json", 'r'))
# out_file = open("database/agent_profiles.json", 'w')

# db_json = {
#     "_default": {}
# }

# for idx, item in enumerate(in_file):
#     new_item = {
#         "first_name": item['first_name'],
#         "last_name": item['last_name'],
#         "age": item['age'],
#         "occupation": item['occupation'],
#         "gender": item['gender'],
#         "gender_pronoun": item['gender_pronoun'],
#         "public_info": item['public_info'],
#         "big_five": item['big_five'],
#         "moral_values": item['moral_values'],
#         "schwartz_personal_values": item['schwartz_personal_values'],
#         "personality_and_values": item['personality_and_values'],
#         "decision_making_style": item['decision_making_style'],
#         "secret": item['secret'],
#         "model_id": item['model_id'],
#         "mbti": item['mbti'],
#     }
#     db_json['_default'][str(idx+1)] = new_item

# json.dump(db_json, out_file, indent=2, ensure_ascii=False)
    
in_file = json.load(open("sotopia_data/environment_profiles.json", 'r'))
out_file = open("database/environment_profiles.json", 'w')

db_json = {
    "_default": {}
}

for idx, item in enumerate(in_file):
    new_item = {
        "codename": item["codename"],
        "source": item["source"],
        "scenario": item["scenario"],
        "agent_goals": item["agent_goals"],
        "relationship": item["relationship"],
        "age_constraint": item["age_constraint"],
        "occupation_constraint": item["occupation_constraint"],
        "agent_constraint": item["agent_constraint"],
    }
    db_json['_default'][str(idx+1)] = new_item

json.dump(db_json, out_file, indent=2, ensure_ascii=False)