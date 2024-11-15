import pandas as pd
import random
from tqdm import tqdm
import os
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

from typing import Any, Dict, List
from langchain.chat_models import ChatOpenAI

class ChatVLLMOpenAI(ChatOpenAI):
    """vLLM OpenAI-compatible API chat client"""
    max_tokens: int | None = None  # type: ignore

    # @property
    # def _default_params(self) -> dict[str, Any]:
    #     """Get the default parameters for calling OpenAI API."""
    #     set_model_value = self.model_name

    #     params = {
    #         "model": set_model_value,
    #         "force_timeout": self.request_timeout,
    #         "stream": self.streaming,
    #         "n": self.n,
    #         "temperature": self.temperature,
    #         **self.model_kwargs,
    #     }
    #     if self.max_tokens is not None:
    #         params["max_tokens"] = self.max_tokens
    
    @property
    def _invocation_params(self) -> Dict[str, Any]:
        """Get the parameters used to invoke the model."""
        openai_creds: Dict[str, Any] = {
            "api_key": self.openai_api_key,
            "api_base": self.openai_api_base,
        }

        return {
            "model": self.model_name,
            **openai_creds,
            **self._default_params,
            "logit_bias": None,
        }

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "chat-vllm-openai"


def get_llm(model, api_key=None, api_org=None, model_path=None, **kwargs):
    if 'gpt' in model:
        api_key = os.environ.get('openai_api_key', None)
        if isinstance(api_org, list):
            api_org = random.choice(api_org)
        print(api_org)
        api_org = os.environ.get(f"openai_api_org_{api_org}", None)
        import openai
        openai.api_key = api_key
        openai.organization = api_org
        llm_model = ChatOpenAI
        llm = llm_model(
            openai_api_key=api_key,
            model=model,
            **kwargs
        )
        return llm
    elif model == 'llama2_70b':
        # tgi
        llm_model = ChatVLLMOpenAI
        llm = llm_model(
            openai_api_key=api_key,
            openai_api_base=api_org,
            **kwargs
        )
        return llm
    elif 'llama' in model or 'vicuna' in model or 'alpaca' in model:
        # vllm
        llm_model = ChatVLLMOpenAI
        llm = llm_model(
            openai_api_key=api_key,
            openai_api_base=api_org,
            model_name=model_path,
            **kwargs
        )
        return llm

def call(prompt_lst, llm_config_func, has_system_prompt=True, model_version='gpt-4-1106-preview', api_key=None, api_org=0, model_path=None, verbose=False):
    llm = get_llm(model=model_version, api_key=api_key, api_org=api_org, model_path=model_path)
    llm = llm_config_func(llm)
    prompts = []
    if has_system_prompt:
        prompts.append(SystemMessage(content=prompt_lst[0]))
        prompt_lst = prompt_lst[1:]
    for idx, prompt in enumerate(prompt_lst):
        if idx % 2 == 0:
            prompts.append(HumanMessage(content=prompt))
        else:
            prompts.append(AIMessage(content=prompt))
    chat_template = ChatPromptTemplate.from_messages(prompts)
    if verbose:
        [print(ii.content) for ii in chat_template.messages]
    chain = (chat_template | llm)
    response = chain.invoke({})
    if verbose:
        print(response.content.strip())
    return response.content.strip()

