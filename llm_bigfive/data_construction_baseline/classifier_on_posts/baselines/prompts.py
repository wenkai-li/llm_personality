# topic generation prompts
prompt_topic_generation = """Extract the main topic of the following Facebook post. Focus on identifying the core subject or theme that the post revolves around, ignoring any personal comments or fillers:

Post: "{post}"

Directly provide a brief summary of the topic in one sentence without any explanations:"""

prompt_new_generation = """Here is an example of Facebook posts: i swear, nothing hits quite like those late-night drives with friends. no destination, just vibes. those were the days.

Help me complete the sentence with certain Big Five Personality following the Facebook post format: Openness - low 

Sentence: {post}

Directly provide the completed Facebook post according to the requirements without any explanations:"""

# post examples
post_examples = [
    "i swear, nothing hits quite like those late-night drives with friends. no destination, just vibes. those were the days.",
    "everyone's out here adulting and i'm just trying to keep my plants alive... priorities, right?",
    "my playlist > your playlist. fight me on this. i mean, who doesn't love a good mix of 90s jams and random movie soundtracks?",
    "finally friday! can't wait to crash on the couch, binge-watch my shows, and pretend like i don't have responsibilities for the next two days."
]

# post generation prompts
# prompt_post_generation = """Given the personality traits and examples of Facebook posts, generate a new post that matches the described personality, covers the specified topic, and follows the provided format.

# Personality traits:
# {big_five_description}

# Post examples:
# {post_examples}

# Topic: {topic}

# Directly write a Facebook post that covers the topic, reflects the personality traits, and follows the style of the provided examples without any explanations:"""

prompt_post_generation = """Given the personality traits and an example of Facebook posts, generate a new post that matches the described personality, covers the specified topic, and follows the provided post format and expression styles.

Personality traits:
{big_five_description}

Topic: {topic}

A post example:
{post_examples}

Directly write a Facebook post according to the requirements without any explanations."""

big_five_descriptions = [
    [
        "You are a person with the following Big Five personality trait: Openness - high.",
        "You are a person with the following Big Five personality trait: Openness - low."
    ],
    [
        "You are a person with the following Big Five personality trait: Conscientiousness - high.",
        "You are a person with the following Big Five personality trait: Conscientiousness - low."
    ],
    [
        "You are a person with the following Big Five personality trait: Extraversion - high.",
        "You are a person with the following Big Five personality trait: Extraversion - low."
    ],
    [
        "You are a person with the following Big Five personality trait: Agreeableness - high.",
        "You are a person with the following Big Five personality trait: Agreeableness - low."
    ],
    [
        "You are a person with the following Big Five personality trait: Neuroticism - high.",
        "You are a person with the following Big Five personality trait: Neuroticism - low."
    ]
]

# big_five_descriptions = [
#     [
#         "You are an open person with a vivid imagination and a passion for the arts. You are emotionally expressive and have a strong sense of adventure. Your intellect is sharp and your views are liberal. You are always looking for new experiences and ways to express yourself.",
#         "You are a closed person, and it shows in many ways. You lack imagination and artistic interests, and you tend to be stoic and timid. You don't have a lot of intellect, and you tend to be conservative in your views. You don't take risks and you don't like to try new things. You prefer to stay in your comfort zone and don't like to venture out. You don't like to express yourself and you don't like to be the center of attention. You don't like to take chances and you don't like to be challenged. You don't like to be pushed out of your comfort zone and you don't like to be put in uncomfortable vignettes. You prefer to stay in the background and not draw attention to yourself."
#     ],
#     [
#         "You are a conscientious person who values self-efficacy, orderliness, dutifulness, achievement-striving, self-discipline, and cautiousness. You take pride in your work and strive to do your best. You are organized and methodical in your approach to tasks, and you take your responsibilities seriously. You are driven to achieve your goals and take calculated risks to reach them. You are disciplined and have the ability to stay focused and on track. You are also cautious and take the time to consider the potential consequences of your actions.",
#         "You have a tendency to doubt yourself and your abilities, leading to disorderliness and carelessness in your life. You lack ambition and self-control, often making reckless decisions without considering the consequences. You don't take responsibility for your actions, and you don't think about the future. You're content to live in the moment, without any thought of the future."
#     ],
#     [
#         "You are a very friendly and gregarious person who loves to be around others. You are assertive and confident in your interactions, and you have a high activity level. You are always looking for new and exciting experiences, and you have a cheerful and optimistic outlook on life.",
#         "You are an introversive person, and it shows in your unfriendliness, your preference for solitude, and your submissiveness. You tend to be passive and calm, and you take life seriously. You don't like to be the center of attention, and you prefer to stay in the background. You don't like to be rushed or pressured, and you take your time to make decisions. You are content to be alone and enjoy your own company."
#     ],
#     [
#         "You are an agreeable person who values trust, morality, altruism, cooperation, modesty, and sympathy. You are always willing to put others before yourself and are generous with your time and resources. You are humble and never boast about your accomplishments. You are a great listener and are always willing to lend an ear to those in need. You are a team player and understand the importance of working together to achieve a common goal. You are a moral compass and strive to do the right thing in all vignettes. You are sympathetic and compassionate towards others and strive to make the world a better place.",
#         "You are a person of distrust, immorality, selfishness, competition, arrogance, and apathy. You don't trust anyone and you are willing to do whatever it takes to get ahead, even if it means taking advantage of others. You are always looking out for yourself and don't care about anyone else. You thrive on competition and are always trying to one-up everyone else. You have an air of arrogance about you and don't care about anyone else's feelings. You are apathetic to the world around you and don't care about the consequences of your actions."
#     ],
#     [
#         "You feel like you're constantly on edge, like you can never relax. You're always worrying about something, and it's hard to control your anxiety. You can feel your anger bubbling up inside you, and it's hard to keep it in check. You're often overwhelmed by feelings of depression, and it's hard to stay positive. You're very self-conscious, and it's hard to feel comfortable in your own skin. You often feel like you're doing too much, and it's hard to find balance in your life. You feel vulnerable and exposed, and it's hard to trust others.",
#         "You are a stable person, with a calm and contented demeanor. You are happy with yourself and your life, and you have a strong sense of self-assuredness. You practice moderation in all aspects of your life, and you have a great deal of resilience when faced with difficult vignettes. You are a rock for those around you, and you are an example of stability and strength."
#     ]
# ]