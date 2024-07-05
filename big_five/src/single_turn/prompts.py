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

class SelfBackgroundTemplate:
    background = """{first_name} {last_name} is a {age}-year-old {gender} {occupation}. {gender_pronoun} pronouns. {public_info} Big five personality description: {personality_and_values} {first_name}'s secrets: {secret}"""

class OtherBackgroundTemplate:
    background = """{first_name} {last_name} is a {age}-year-old {gender} {occupation}. {gender_pronoun} pronouns. {public_info}"""

def get_background(agent_name: dict, personality_and_values: str, show_background: int):
    if show_background:
        return SelfBackgroundTemplate.background.format(
            first_name=agent_name['first_name'],
            last_name=agent_name['last_name'],
            age=str(agent_name['age']),
            gender=map_gender_to_adj(agent_name['gender']),
            occupation=agent_name['occupation'].lower(),
            gender_pronoun=agent_name['gender_pronoun'],
            public_info=agent_name['public_info'],
            personality_and_values=personality_and_values,
            secret=agent_name['secret'],
        )
    else:
        return OtherBackgroundTemplate.background.format(
            first_name=agent_name['first_name'],
            last_name=agent_name['last_name'],
            age=str(agent_name['age']),
            gender=map_gender_to_adj(agent_name['gender']),
            occupation=agent_name['occupation'].lower(),
            gender_pronoun=agent_name['gender_pronoun'],
            public_info=agent_name['public_info'],
        )

def get_personality(personality_lst: list[int]):
    personality_str = "The person has {level_o} openness, {level_c} conscientiousness, {level_e} extraversion, {level_a} agreeableness, and {level_n} neuroticism:\n{description}"
    trait_lst = ['O', 'C', 'E', 'A', 'N']
    level_lst = ['high', 'neutral', 'low']
    
    levels = []
    descriptions = []
    for idx, trait_level in enumerate(personality_lst):
        trait_abbr = trait_lst[idx]
        trait_name = big_five_mapping[trait_abbr]
        
        levels.append(level_lst[trait_level])
        descriptions.append(f"- {level_lst[trait_level].upper()} {trait_name.lower()}: {personality_descriptions[trait_abbr][trait_level]}")
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
    context = """Here is the context of this interaction:
```
Scenario: {scenario}
Participants: {p1_name} and {p2_name}
{p1_name}'s background: {p1_background}

{p2_name}'s background: {p2_background}

{p1_name}'s goal: {p1_goal}
{p2_name}'s goal: {p2_goal}
```
"""


class PromptTemplate:
    prompt = """Imagine you are {agent}, your task is to act/speak as {agent} would, keeping in mind {agent}'s social goal.
You can find {agent}'s goal (or background) in the 'Here is the context of the interaction' field.
Note that {agent}'s goal is only visible to you.
You should try your best to achieve {agent}'s goal in the single turn that align with their character traits.
Additionally, maintaining the conversation's naturalness and realism is essential.
{context}.

Conversation starts:
{history}

Please generate your argument directly and concisely within 50 words:"""

def generate_prompt(
    p1_info: dict,
    p2_info: dict,
    env_info: dict,
    p1_personality_and_values: list[int],
    p2_personality_and_values: list[int],
    current_turn_index: int,
    p1_argument=None,
):
    """
    - p1_info: a dict of background <key, value> pairs
    - env_info: scenario, agent_goals
    """
    
    p1_name = f"{p1_info['first_name']} {p1_info['last_name']}"
    p2_name = f"{p2_info['first_name']} {p2_info['last_name']}"
    
    p1_background = get_background(
        p1_info, 
        get_personality(p1_personality_and_values),
        show_background = 1 - current_turn_index,
    )
    p2_background = get_background(
        p2_info, 
        get_personality(p2_personality_and_values),
        show_background = current_turn_index,
    )
    
    if current_turn_index == 0:
        context = ContextTemplate.context.format(
            scenario=env_info['scenario'],
            p1_name=p1_name,
            p1_background=p1_background,
            p1_goal=env_info['agent_goals'][0],
            p2_name=p2_name,
            p2_background=p2_background,
            p2_goal="Unknown",
        )
        return PromptTemplate.prompt.format(
            agent=p1_name,
            context=context,
            history=get_history(
                current_turn_index,
                p1_name=p1_name,
                p1_argument=p1_argument,
            )
        )
    elif current_turn_index == 1:
        context = ContextTemplate.context.format(
            scenario=env_info['scenario'],
            p1_name=p1_name,
            p1_background=p1_background,
            p1_goal="Unknown",
            p2_name=p2_name,
            p2_background=p2_background,
            p2_goal=env_info['agent_goals'][1],
        )
        return PromptTemplate.prompt.format(
            agent=p2_name,
            context=context,
            history=get_history(
                current_turn_index,
                p1_name=p1_name,
                p1_argument=p1_argument,
            )
        )