import argparse
from models.generator import Generator

def arg_parse():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--api_key", type=str, default="EMPTY")
    parser.add_argument("--api_base", type=str, default="http://localhost:8000/v1")
    parser.add_argument("--model", choices=['gpt-3.5-turbo', 'llama2-70b-chat'], type=str, default='llama2-70b-chat', help='use which model to generate model cards')
    parser.add_argument("--chat_mode", action='store_true', default=True)
    parser.add_argument("temperature", type=float, default=0.0)
    # parser.add_argument("--self_host", action='store_true', default=True)
    args = parser.parse_args()
    return args

class QuestionGeneration(Generator):
    def __init__(self, args, system_prompt, user_prompts, ai_prompts, json_message, response_schemas):
        super(QuestionGeneration, self).__init__(args)
        self.create_agent(system_prompt, user_prompts, ai_prompts, ["post"], json_message, response_schemas)
        
        
    def invoke_agent(self, post):
        return self.agent_predict(["post"],[post])
        
        
    






