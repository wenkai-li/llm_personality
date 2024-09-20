import json

in_data = [json.loads(i) for i in open("/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/llama3_8b_v3/out_llama3_8b_v3.jsonl", 'r')]
out_f = open("out_direct.jsonl", 'a')

for i in in_data:
    info = {"post": i['prompt1'].split('\n\nPost: "')[-1].split('"\n\nDirect provide')[0]}
    json.dump(info, out_f)
    out_f.write("\n")
    out_f.flush()

