import sys
import os
sys.path.append("../../")
from new_sotopia.databases.persistent_profile import AgentProfile, EnvironmentProfile
from typing import Any
from new_sotopia.samplers import UniformSampler
from new_sotopia.server import run_async_server
from datasets import load_dataset, DatasetDict, load_from_disk
from new_sotopia.generation_utils.generate import agenerate_env_profile
from tqdm import tqdm
import asyncio

async def gen_env_profile(data) -> None:
    env_profile = await agenerate_env_profile(
        model_name="llama3_70b",
        inspiration_prompt=data['narrative']
    )
    env_profile = env_profile[0]
    env_profile.init_profile_store()
    env_profile.db.insert_unique(env_profile.dict())
    return env_profile

async def main():
    data = load_from_disk("/data/user_data/wenkail/llm_personality/soda_data/sample_5000")
    
    for d in tqdm(data['sample']):
        await gen_env_profile(d)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())