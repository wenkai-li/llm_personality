import argparse
from models.generator import Generator


class PersonalityImitation(Generator):
    def __init__(self, args, system_prompt, questions, posts, user_prompt, ai_prompt, json_message, response_schemas):
        super(PersonalityImitation, self).__init__(args)
        self.create_agent(system_prompt, questions + user_prompt, posts + ai_prompt, ["mbti"], json_message, response_schemas)
        
        
    def invoke_agent(self, mbti):
        return self.agent_predict(["mbti"],[mbti])
        
        