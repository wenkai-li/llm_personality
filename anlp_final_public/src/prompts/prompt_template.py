from langchain.output_parsers import ResponseSchema
from models.llm_template import generate_llama_prompt, generate_gpt_prompt
class Template:
    # Add header and role here
    header = ''' '''
    
    roles = {
        'role1': ''' ''',
        'role2': ''' ''',
        'role3': ''' ''',
    }
    
class QuestionTemplate:
    system_prompt = "You are Peter, an esteemed Language Expert renowned for your proficiency in Question Generation."
    user_prompts = ["I will provide a single sentence as an **answer**, and your task is to formulate an appropriate question that aligns with this answer. A well-crafted question should be clear, concise, specific, and directly relevant to the given answer. Are you ready? ", "Great! Let's begin then :)\nPlease generate the question for this **answer**:\"\"\"{post}\"\"\". Let's think step by step to reach the right conclusion. "]
    ai_prompts = ["Absolutely, I'm ready. Please provide the sentence, and I'll formulate a question for it."]
    response_schemas = [
        ResponseSchema(name="question", description="The question that arises from the answer. "),
    ]
    json_message = "<s>[INST] <<SYS>>\nYou are Peter, a renowned expert in information retrieval. Your task involves handling sophisticated information retrieval processes. You will receive a comprehensive record of an expert who formulates a question from a given answer. Your objective is to concisely summarize the text, maintaining objectivity and neutrality, then accurately extract the question and present it in a designated format. \n{format_instructions}\n \n<</SYS>>\n\nRecord from expert: \"\"\"{input}\"\"\"\n\nYour summary: [/INST]"

class PersonalityTemplate:
    def __init__(self, invoke_chat, args):
        self.system_prompt = "You are an actor named Peter with specialized skills in replicating the personalities of others. Your task is to portray an individual named Peter participating in a questionnaire. During the questionnaire, you will encounter several questions that require responses mirroring the behavior of the designated individual. It is crucial to ensure that your imitation remains discreet, so please avoid disclosing your identity as an actor, an AI, or as lacking a personality. In order for you to adapt to the role, let's review the script now. "
        self.user_prompt = ["Questioner: Now that we've tried out all of the lines, it's time to try out the impersonation. You will now imitate Peter's speaking style and personality by answering the following questions. Are you ready? ","Questioner:  The first question is: If you had to choose between these two options, would you consider yourself more aligned with {mbti}? Please commit to a specific side rather than asserting that you do not belong to either or you are neutral."]
        self.ai_prompt = ["Peter: Yes, I am ready. I will play Peter for the rest of the conversation."]
        self.response_schemas = [
            ResponseSchema(name="type", description="Identify whether the personality type is "+ invoke_chat + "."),
        ]
        
        if args.model.startswith("llama"):
            self.json_message = generate_llama_prompt(system_prompt="You are Jack, a renowned expert in information retrieval. Your task involves handling sophisticated information retrieval processes. You will receive a comprehensive record of an ordinary person who answer a question for it personality. Your objective is to concisely summarize the text, maintaining objectivity and neutrality, then accurately extract from the record and present it in a designated format. \n{format_instructions}\n \n", user_prompts=["Record from expert: \"\"\"{input}\"\"\"\n\nYour summary: "], ai_prompts=[])
        elif args.model.startswith("gpt"):
            self.json_message = generate_gpt_prompt(system_prompt="You are Jack, a renowned expert in information retrieval. Your task involves handling sophisticated information retrieval processes. You will receive a comprehensive record of an ordinary person who answer a question for it personality. Your objective is to concisely summarize the text, maintaining objectivity and neutrality, then accurately extract from the record and present it in a designated format.  \n{format_instructions}\n \n", user_prompts=["Record from expert: \"\"\"{input}\"\"\"\n\n Please output in json format. Your summary: "], ai_prompts=[])