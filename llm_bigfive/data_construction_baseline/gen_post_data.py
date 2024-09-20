import time
import openai
import json
import torch
import random
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from tqdm import tqdm

from prompts import *

class GPT:
    def __init__(self, model_id):
        with open("/home/jiaruil5/openai_key.txt", 'r') as file:
            content = []
            for i in file.readlines():
                content.append(i.strip())
            openai.api_key = content[0]
            openai.organization = content[1]
        
        
        self.client = openai.chat.completions
        self.model_id = model_id
        self.max_retries = 5
        
    
    def generate(self, messages, **inference_config):
        curr_retries = 0
        while True:
            try:
                response = self.client.create(
                    model = self.model_id,
                    messages = messages,
                    temperature=0.0,
                    max_tokens=2048,
                    **inference_config,
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
                if curr_retries >= self.max_retries:
                    print("EXITING...")
                    exit(1)
                else:
                    print("RETRYING...")
                    curr_retries += 1
                    time.sleep(5)

class LLAMA3():
    def __init__(self, args):
        """
        args: model, model_mode, model_path, model_lora_path, cache_dir
        - parser.add_argument('--model', required=True, type=str, default='text-davinci-003', help='The name of the model to test')
        - parser.add_argument('--cache_dir', type=str, default=None)
        - parser.add_argument('--model_mode', type=str, default='direct', help='direct, train_xxxxx, or prompt_xxxxx')
        - parser.add_argument('--model_path', type=str, default=None)
        - parser.add_argument('--model_lora_path', type=str, default=None)
        """
        
        self.args = args
        assert args.model in ['llama3_8b', 'llama3_70b']

        self.tokenizer = AutoTokenizer.from_pretrained(
            args.model_path,
            cache_dir=args.cache_dir
        )
        self.terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        
        
        self.model = AutoModelForCausalLM.from_pretrained(
            args.model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            cache_dir=args.cache_dir
        )
        if args.model_lora_path:
            self.model = PeftModel.from_pretrained(
                self.model,
                args.model_lora_path
            )
        self.model.eval()
    
    
    def generate(self, messages, **gen_kwargs):
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device) # type: ignore

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=1024,
            eos_token_id=self.terminators,
            do_sample=False,
            **gen_kwargs
        )
        response = outputs[0][input_ids.shape[-1]:]
        result = self.tokenizer.decode(response, skip_special_tokens=True)
        return result

class PostDataGenerator():
    def __init__(self, model):
        self.model = None
        if model == "llama3_70b":
            class Args:
                model = "llama3_70b"
                model_path = "/compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/"
                cache_dir = None
                model_lora_path = None
            self.model = LLAMA3(Args)
        elif model == "llama3_8b":
            class Args:
                model = "llama3_8b"
                model_path = "/data/models/huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
                cache_dir = None
                model_lora_path = None
            self.model = LLAMA3(Args)
        elif model == "gpt-4o-mini":
            self.model = GPT(model)
        self.model_id = model
    
    
    def load_data(self, store_path):
        
        new_data = []
        for trait in ['o', 'c', 'e', 'a', 'n']:
            file_path = f"/data/user_data/wenkail/llm_personality/generator/data/outputs/generated_predictions_{trait}.jsonl"
            data = [json.loads(i) for i in open(file_path, 'r')]
            data = random.sample(data, 200)
            for i in data:
                post = i['prompt'].split("- high\n")[-1].split("- low\n")[-1].split("assistant\n\n")[0] + " " + i['label']
                level = "high" if "- high\n" in i['prompt'] else 'low'
                new_data.append({
                    "post": post,
                    "level": level,
                    "trait": trait
                })
                
        json.dump(new_data, open(store_path, 'w'), ensure_ascii=False, indent=2)
        return new_data
    
    def gen_post_data(self, data, out_file):
        out_f = open(out_file, 'a')
        for item in tqdm(data):
            # gen topics
            prompt1 = prompt_topic_generation.format(post = item['post'])
            print("Prompt1:", prompt1)
            topic = self.model.generate([
                {"role": "user", "content": prompt1}
            ])
            print("Topic:", topic)
            
            # gen_posts
            trait_idx = ['o', 'c', 'e', 'a', 'n'].index(item['trait'])
            level_idx = ['high', 'low'].index(item['level'])
            prompt2 = prompt_post_generation.format(
                big_five_description = big_five_descriptions[trait_idx][level_idx],
                post_examples = "- " + "- ".join(post_examples[:1]),
                topic = topic
            )
            print("Prompt2:", prompt2)
            post = self.model.generate([
                {"role": "user", "content": prompt2}
            ])
            print("Post:", post)
            info = {
                "prompt1": prompt1,
                "topic": topic,
                "prompt2": prompt2,
                "post": post,
            }
            json.dump(info, out_f, ensure_ascii=False)
            out_f.write("\n")
            out_f.flush()
            

if __name__ == "__main__":
    generator = PostDataGenerator('gpt-4o-mini')
    store_path = "/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/data_input.json"
    # generator.load_data(store_path)
    data = json.load(open(store_path, 'r'))
    generator.gen_post_data(data, "/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/out_gpt4omini_v3.jsonl")
    
    # generator = PostDataGenerator('llama3_8b')
    # store_path = "/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/data_input.json"
    # # generator.load_data(store_path)
    # data = json.load(open(store_path, 'r'))
    # generator.gen_post_data(data, "/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/out_llama3_8b_v3.jsonl")