import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    padding_side="left",
    cache_dir = "/data/user_data/jiaruil5/.cache/",
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    cache_dir = "/data/user_data/jiaruil5/.cache/"
)

lora_model_path = "/data/user_data/wenkail/llm_personality/generator/generator_whole_o_1e-6/"
model = PeftModel.from_pretrained(model, lora_model_path)
model.eval()

messages = [
    {
        "role": "user", "content": "Help me complete the sentence with certain Big Five Personality: Openness - high\nmy phones acting a little"
    }
]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt = True,
    return_tensors = "pt",
).to(model.device)

print(input_ids)
outputs = model.generate(
    input_ids,
    # do_sample=True,
    do_sample=False,
    temperature=0.95,
    top_p=0.7,
    top_k=50,
    max_new_tokens = 1024,
    repetition_penalty = 1.0,
    length_penalty = 1.0
)
print(outputs[0])
response = outputs[0][input_ids.shape[-1]:]
result = tokenizer.decode(response, skip_special_tokens=True)
print(result)