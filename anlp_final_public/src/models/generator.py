from models.llm_template import generate_llama_prompt, generate_gpt_prompt
import openai
import os
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser

class Generator():
    def __init__(self, args):
        self.args = args
        self.llm = None
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        llm_model = None
        self.template = None
        if self.args.model.startswith("llama"):
            openai.api_key = args.api_key
            openai.api_base = args.api_base
            if self.args.chat_mode:
                from langchain.chat_models import ChatOpenAI
                llm_model = ChatOpenAI
            else:
                from langchain.llms.vllm import VLLMOpenAI
                llm_model = VLLMOpenAI
            self.llm = llm_model(
                    openai_api_key=self.args.api_key,
                    openai_api_base=self.args.api_base,
                    model_name=openai.Model.list()['data'][0]['id'],
                    model_kwargs=self.args.model_kwargs,
                    # , "Human", "nHuman"
                    max_tokens = self.args.max_tokens,
                    temperature= self.args.temperature,
                    top_p = self.args.top_p,
                    streaming=True,
                    verbose=True,
                )
                
            # self.llm = VLLM(model=self.llm, tensor_parallel_size=4, gpu_memory_utilization=0.95, top_k=1,
            #                                         stop=['\n', '.', '<\s>', 'nHuman', 'Human'],max_new_tokens=7)
        elif self.args.model.startswith("gpt"):
            openai.api_key = os.getenv(args.api_key)
            if args.chat_mode:
                from langchain.chat_models import ChatOpenAI
                llm_model = ChatOpenAI
            else:
                from langchain.llms.openai import OpenAI
                llm_model = OpenAI
            self.llm = llm_model(
                    model=self.args.model,
                    # model_kwargs=self.args.model_kwargs,
                    # , "Human", "nHuman"
                    max_tokens = self.args.max_tokens,
                    temperature= self.args.temperature,
                    streaming=True,
                    verbose=True,
                
            )
        else:
            from langchain.llms.vllm import VLLM
            self.llm =self.args.llm
                    
        if self.llm is None:
            raise NotImplementedError("Model not found.")
        else:
            print("Using model: {}".format(self.llm))
            
    def create_agent(self, system_prompt, user_prompts, ai_prompts, input_variables, json_message=None, response_schemas=None):
        if self.args.chat_mode==False:
            prefix_temp = generate_llama_prompt(system_prompt=system_prompt, user_prompts=user_prompts, ai_prompts = ai_prompts)
        else:
            prefix_temp = generate_gpt_prompt(system_prompt=system_prompt, user_prompts=user_prompts, ai_prompts = ai_prompts)
        if self.args.chat_mode:
            prompt = ChatPromptTemplate(messages=prefix_temp, input_variables=input_variables)
        else:
            prompt = PromptTemplate(input_variables=input_variables, template=prefix_temp)
        if json_message == None or response_schemas==None:
            self.agent = prompt | self.llm
        else:
            self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
            if self.args.chat_mode:
                json_prompt = ChatPromptTemplate(messages=json_message, input_variables=['input'],
                                     partial_variables={"format_instructions": self.output_parser.get_format_instructions()})
            else:
                json_prompt = PromptTemplate(template=json_message, input_variables=['input'],
                                     partial_variables={"format_instructions": self.output_parser.get_format_instructions()})
                
            json_chain = json_prompt | self.llm | self.output_parser
            self.agent = {"input": prompt | self.llm} | json_chain
        

    def agent_predict(self, input_variables, inputs):
        input_message = {}
        for key, value in zip(input_variables,inputs):
            input_message[key] = value
        return self.agent.invoke(input_message)