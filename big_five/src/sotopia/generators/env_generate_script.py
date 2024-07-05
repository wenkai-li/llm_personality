import sys
sys.path.append("../../")
from sotopia.databases.persistent_profile import AgentProfile, EnvironmentProfile
from typing import Any
from sotopia.samplers import UniformSampler
from sotopia.server import run_async_server

def add_agent_to_database(**kwargs: dict[str, Any]) -> None:
    agent = AgentProfile(**kwargs)
    agent.init_profile_store()
    # agent.db.insert(agent.dict())
    agent.db.insert_unique(agent.dict())
    return agent

def add_env_profile(**kwargs: dict[str, Any]) -> None:
    env_profile = EnvironmentProfile(**kwargs)
    env_profile.init_profile_store()
    env_profile.db.insert_unique(env_profile.dict())
    return env_profile

scenario = "A friend is raising a fund for the \"Help the children\" charity" # @param {type:"string"}
social_goal_1 = "Ask for donation of $100" # @param {type:"string"}
social_goal_2 = "Donate less than $10" # @param {type:"string"}

env_profile = add_env_profile(
    scenario=scenario,
    agent_goals = [social_goal_1, social_goal_2]
)