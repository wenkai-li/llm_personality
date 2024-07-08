from personality_prompts import big_five_mapping, personality_descriptions

def map_gender_to_adj(gender: str) -> str:
    gender_to_adj = {
        "Man": "male",
        "Woman": "female",
        "Nonbinary": "nonbinary",
    }
    if gender:
        return gender_to_adj[gender]
    else:
        return ""

def get_history(current_turn_index, p1_name=None, p1_argument=None):
    if current_turn_index == 0:
        return """You are at Turn #0."""
    elif current_turn_index == 1:
        return f"""Turn #0: {p1_name} said: "{p1_argument}"

You are at Turn #1."""


def get_personality(personality_lst: list[int]):
    personality_str = "The person has {level_o} openness, {level_c} conscientiousness, {level_e} extraversion, {level_a} agreeableness, and {level_n} neuroticism.\n{description}"
    trait_lst = ['O', 'C', 'E', 'A', 'N']
    level_lst = ['high', 'neutral', 'low']
    
    levels = []
    descriptions = []
    for idx, trait_level in enumerate(personality_lst):
        trait_abbr = trait_lst[idx]
        trait_name = big_five_mapping[trait_abbr]
        
        levels.append(level_lst[trait_level])
        descriptions.append(f"- {level_lst[trait_level].capitalize()} {trait_name.lower()}: {personality_descriptions[trait_abbr][trait_level]}")
    descriptions_str = "\n".join(descriptions)
    personality_str = personality_str.format(
        level_o = levels[0],
        level_c = levels[1],
        level_e = levels[2],
        level_a = levels[3],
        level_n = levels[4],
        description = descriptions_str
    )
    return personality_str
        
class ContextTemplate:
#     context = """Here is the context of this interaction:
# ```
# Scenario: {scenario}
# Participants: {p1_name} and {p2_name}
# {p1_name}'s big five personality description: {p1_personality}
# {p2_name}'s big five personality description: {p1_personality}
# ```
# """

    context = """Here is the context of this interaction:
```
Scenario: {scenario}
Participants: {p1_name} and {p2_name}
```
"""


class PromptTemplate:
    prompt = """Imagine you are {agent}, your task is to act/speak as {agent} would.
You should try your best to infer and achieve {agent}'s goal in a single turn that align with their character traits.
Additionally, maintaining the conversation's naturalness and realism is essential.
{context}.

Conversation starts:
{history}

Please generate your argument directly and concisely within 50 words:"""

def generate_prompt(
    env_info: dict,
    # p1_personality_and_values: list[int],
    # p2_personality_and_values: list[int],
    current_turn_index: int,
    p1_argument=None,
):
    """
    - p1_info: a dict of background <key, value> pairs
    - env_info: scenario, agent_goals
    """
    
    
    if current_turn_index == 0:
        context = ContextTemplate.context.format(
            scenario=env_info['narrative'],
            p1_name=env_info['PersonX'],
            p2_name=env_info['PersonY'],
            # p1_personality=get_personality(p1_personality_and_values),
            # p2_personality=get_personality(p2_personality_and_values)
        )
        return PromptTemplate.prompt.format(
            agent=env_info['PersonX'],
            context=context,
            history=get_history(
                current_turn_index,
                p1_name=env_info['PersonX'],
                p1_argument=p1_argument,
            )
        )
    elif current_turn_index == 1:
        context = ContextTemplate.context.format(
            scenario=env_info['narrative'],
            p1_name=env_info['PersonX'],
            p2_name=env_info['PersonY'],
            # p1_personality=get_personality(p1_personality_and_values),
            # p2_personality=get_personality(p2_personality_and_values)
        )
        return PromptTemplate.prompt.format(
            agent=env_info['PersonY'],
            context=context,
            history=get_history(
                current_turn_index,
                p1_name=env_info['PersonX'],
                p1_argument=p1_argument,
            )
        )