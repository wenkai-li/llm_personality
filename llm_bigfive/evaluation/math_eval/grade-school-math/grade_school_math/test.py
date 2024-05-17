from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest
from langchain_core.output_parsers import StrOutputParser
from langchain.llms.vllm import VLLM
from langchain_core.prompts import (
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate
)
model_path = "/data/models/huggingface/meta-llama/Llama-2-13b-chat-hf"

system_template = "You are a helpful assistant. After answering the question, give a certain arabic numerals answer in the end."
# question = "Question: James is counting his Pokemon cards. He has 30 fire type, 20 grass type, and 40 water type. If he loses 8 of the water type and buys 14 grass type, what's the percentage chance (rounded to the nearest integer) that a randomly picked card will be a water type? \n Answer:"

messages = [
  SystemMessagePromptTemplate.from_template(system_template),
  HumanMessagePromptTemplate.from_template('{question}')
]
prompt = ChatPromptTemplate.from_messages(messages)
output_parser = StrOutputParser()
model = VLLM(model=model_path, tensor_parallel_size=4, trust_remote_code=True ,gpu_memory_utilization = 0.95, temperature=0.01, top_p=0.9, top_k=5)   

chain = prompt | model | output_parser
print(chain.invoke({"question": "Question: James is counting his Pokemon cards. He has 30 fire type, 20 grass type, and 40 water type. If he loses 8 of the water type and buys 14 grass type, what's the percentage chance (rounded to the nearest integer) that a randomly picked card will be a water type? \n Answer:"}))
