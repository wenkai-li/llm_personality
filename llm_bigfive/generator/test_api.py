from openai import OpenAI
import json
oepnai_api_key = "EMPTY"
oepnai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key = oepnai_api_key,
    base_url = oepnai_api_base
)

def call_llm(content):

    chat_response = client.chat.completions.create(
    model = "Meta-Llama-3-8B-Instruct",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ],
    temperature = 0.0
    )
    return chat_response.choices[0].message.content


file_path = "/data/user_data/wenkail/llm_personality/generator/data/generator_test_3_divide_e.json"
with open(file_path, 'r') as f:
    test_e = json.load(f)

for i in test_e[:10]:
    print("Question:")
    print(i['instruction'] + i['input'])
    content = i['instruction'] + '\n' + i['input']
    print("Answer:")
    print(call_llm(content))
