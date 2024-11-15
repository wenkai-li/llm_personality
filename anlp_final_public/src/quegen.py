from types import SimpleNamespace
from models.question_generation import *
from prompts.prompt_template import QuestionTemplate
from data_processing.preprocess import KaggleDataset
from tqdm import tqdm
import csv

args = SimpleNamespace(
    api_key = 'sk-',
    api_base='http://babel-0-27:5050/v1',
    model='llama2-70b-chat',
    chat_mode = False,
    max_tokens = 256,
    model_kwargs = {"stop": ["<\s>"]},
    temperature=0
)

# openai.api_key = args.api_key
# openai.api_base = args.api_base
QGtemplate = QuestionTemplate()

generator = QuestionGeneration(args, system_prompt=QGtemplate.system_prompt, user_prompts=QGtemplate.user_prompts, ai_prompts=QGtemplate.ai_prompts, json_message=QGtemplate.json_message ,response_schemas = QGtemplate.response_schemas)

dataset = KaggleDataset()
file_path = '/home/zw3/ANLP_Final/data/kaggleWithQuestion.csv'
file =  open(file_path, 'a', newline='')
writer = csv.writer(file, delimiter='\t')

# Write CSV Header
writer.writerow(['posts', 'questions', 'label0', 'label1', 'label2', 'label3'])
file.close()
for row in tqdm(dataset.poster_data[40:100]):
    questions = []
    for post in row['posts']:
        try:
            question = generator.invoke_agent(post)
            if question['question'] != None:
                questions.append(question['question'])
            else: 
                questions.append("N/A")
        except:
            questions.append("N/A")
        print(questions[-1])
    row['questions'] = questions
    file = open(file_path, 'a', newline='')
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(['|||'.join(row['posts']), '|||'.join(row['questions']), row['label0'], row['label1'], row['label2'], row['label3']])
    file.close()
    
