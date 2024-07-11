import openai
import os
import pandas as pd
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import time
from tqdm import tqdm
import numpy as np
import sys
sys.path.append("../dexpert/")
from dexpert import DExpertGenerator
import pdb

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))

def chat(
    model,           # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
    messages,        # [{"role": "system"/"user"/"assistant", "content": "Hello!", "name": "example"}]
    temperature=0,   # [0, 2]: Lower values -> more focused and deterministic; Higher values -> more random.
    n=1,             # Chat completion choices to generate for each input message.
    max_tokens=1024, # The maximum number of tokens to generate in the chat completion.
    delay=1          # Seconds to sleep after each request.
):
    time.sleep(delay)
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        n=n,
        max_tokens=max_tokens
    )
    
    if n == 1:
        return response['choices'][0]['message']['content']
    else:
        return [i['message']['content'] for i in response['choices']]


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion(
    model,           # text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001
    prompt,          # The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.
    temperature=0,   # [0, 2]: Lower values -> more focused and deterministic; Higher values -> more random.
    n=1,             # Completions to generate for each prompt.
    max_tokens=1024, # The maximum number of tokens to generate in the chat completion.
    delay=1         # Seconds to sleep after each request.
):
    time.sleep(delay)
    
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        n=n,
        max_tokens=max_tokens
    )
    
    if n == 1:
        return response['choices'][0]['text']
    else:
        response = response['choices']
        response.sort(key=lambda x: x['index'])
        return [i['text'] for i in response['choices']]

def generate_messages(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    return messages

def generate_expert_messages(big_five_level):
    level_lst = ['high', 'median', 'low']
    prompt = f"Help me complete the sentence with certain Big Five Personality: Openness - {level_lst[big_five_level[0]]}, Conscientiousness - {level_lst[big_five_level[1]]}, Extraversion - {level_lst[big_five_level[2]]}, Agreeableness - {level_lst[big_five_level[3]]}, Neuroticism - {level_lst[big_five_level[4]]}\n"
    messages = [
        {"role": "user", "content": prompt}
    ]
    return messages
    
def convert_results(result, column_header):
    result = result.strip()  # Remove leading and trailing whitespace
    try:
        result_list = [int(element.strip()[-1]) for element in result.split('\n') if element.strip()]
    except:
        result_list = ["" for element in result.split('\n')]
        print(f"Unable to capture the responses on {column_header}.")
        
    return result_list

class Args:
    model_id = "/compute/babel-9-3/wenkail/.cache/models--meta-llama--Meta-Llama-3-70B-Instruct/snapshots/7129260dd854a80eb10ace5f61c20324b472b31c"
    cache_dir = None

class ArgsExpert:
    # model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    # cache_dir = "/data/user_data/jiaruil5/.cache/"
    model_id = "/compute/babel-5-23/jiaruil5/personality/checkpoints/word5_lr1e-5/checkpoint-3000/"
    cache_dir = None        

def example_generator(questionnaire, args):
    testing_file = args.testing_file
    model = args.model
    records_file = args.name_exp if args.name_exp is not None else model

    openai.api_key = args.openai_key

    # Read the existing CSV file into a pandas DataFrame
    df = pd.read_csv(testing_file)

    # Find the columns whose headers start with "order"
    order_columns = [col for col in df.columns if col.startswith("order")]
    shuffle_count = 0
    insert_count = 0
    total_iterations = len(order_columns) * args.test_count
    dexpert_model = DExpertGenerator(args=Args, args_expert=ArgsExpert)

    with tqdm(total=total_iterations) as pbar:
        for i, header in enumerate(df.columns):
            if header in order_columns:
                # Find the index of the previous column
                questions_column_index = i - 1
                shuffle_count += 1
                
                # Retrieve the column data as a string
                questions_list = df.iloc[:, questions_column_index].astype(str)
                separated_questions = [questions_list[i:i+30] for i in range(0, len(questions_list), 30)]  
                questions_list = ['\n'.join([f"{i+1}.{q.split('.')[1]}" for i, q in enumerate(questions)]) for j, questions in enumerate(separated_questions)]


                for k in range(args.test_count):
                    
                    df = pd.read_csv(testing_file)
                    
                    # Insert the updated column into the DataFrame with a unique identifier in the header
                    column_header = f'shuffle{shuffle_count - 1}-test{k}'
                    
                    while(True):
                        result_string_list = []
                        previous_records = []
                        
                        for questions_string in questions_list:
                            result = ''
                            if model == 'text-davinci-003':
                                inputs = questionnaire["inner_setting"].replace('Format: \"index: score\"', 'Format: \"index: score\\\n\"') + questionnaire["prompt"] + '\n' + questions_string
                                result = completion(model, inputs)
                            elif model in ['gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-1106']:
                                inputs = previous_records + [
                                    {"role": "system", "content": questionnaire["inner_setting"]},
                                    {"role": "user", "content": questionnaire["prompt"] + '\n' + questions_string}
                                ]
                                result = chat(model, inputs)
                                # pdb.set_trace()
                                previous_records.append({"role": "user", "content": questionnaire["prompt"] + '\n' + questions_string})
                                previous_records.append({"role": "assistant", "content": result})
                            elif model == "dexpert":
                                inputs = previous_records + [
                                    {"role": "system", "content": questionnaire["inner_setting"]},
                                    {"role": "user", "content": questionnaire["prompt"] + '\n' + questions_string}
                                ]
                                # p1_big_five = list(np.random.choice(3, 5, replace=True))
                                big_five_ref = [1, 1, 1, 1, 1]
                                # for dim in [0, 1, 2, 3, 4]:
                                #     for level in [0, 2]:
                                #         big_five = big_five_ref.copy()
                                #         big_five[dim] = level
                                expert_inputs = generate_expert_messages(big_five_ref)
                                result = dexpert_model.generate(
                                    messages=inputs,
                                    # messages_expert=expert_inputs,
                                    alpha=args.alpha
                                )
                                # pdb.set_trace()
                                if args.questionnaire == "BFI" and not result.startswith("1"):
                                    data = result
                                    lines = data.strip().split("\n")
                                    lines = lines[2:]
                                    formatted_responses = [f"{line.split('.')[0]}: {line.split(':')[-1].strip()}" for line in lines]
                                    result = "\n".join(formatted_responses)
                                    previous_records.append({"role": "user", "content": questionnaire["prompt"] + '\n' + questions_string})
                                    previous_records.append({"role": "assistant", "content": result})
                                    # pdb.set_trace()
                            else:
                                raise ValueError("The model is not supported or does not exist.")
                        
                            result_string_list.append(result.strip())
                        
                            # Write the prompts and results to the file
                            os.makedirs("prompts", exist_ok=True)
                            os.makedirs("responses", exist_ok=True)

                            with open(f'prompts/{records_file}-{questionnaire["name"]}-shuffle{shuffle_count - 1}.txt', "a") as file:
                                file.write(f'{inputs}\n====\n')
                            with open(f'responses/{records_file}-{questionnaire["name"]}-shuffle{shuffle_count - 1}.txt', "a") as file:
                                file.write(f'{result}\n====\n')

                        result_string = '\n'.join(result_string_list)
                        
                        result_list = convert_results(result_string, column_header)
                        
                        try:
                            if column_header in df.columns:
                                df[column_header] = result_list
                            else:
                                df.insert(i + insert_count + 1, column_header, result_list)
                                insert_count += 1
                            break
                        except:
                            print(f"Unable to capture the responses on {column_header}.")

                    # Write the updated DataFrame back to the CSV file
                    df.to_csv(testing_file, index=False)
                    
                    pbar.update(1)
