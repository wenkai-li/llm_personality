from transformers import AutoTokenizer

cache_dir = "/data/user_data/jiaruil5/.cache/"

tokenizer1 = AutoTokenizer.from_pretrained("google/gemma-2b", cache_dir = cache_dir, token="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")
tokenizer2 = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct", cache_dir=cache_dir)

print(len(tokenizer1))
print(len(tokenizer2))
tokens_1 = set(tokenizer1.get_vocab().keys())
tokens_2 = set(tokenizer2.get_vocab().keys())

overlap_tokens = tokens_1.intersection(tokens_2)
unique_tokens_1 = tokens_1 - tokens_2
unique_tokens_2 = tokens_2 - tokens_1

print(f"Number of overlapping tokens: {len(overlap_tokens)}")
print(f"Number of unique tokens in tokenizer 1: {len(unique_tokens_1)}")
print(f"Number of unique tokens in tokenizer 2: {len(unique_tokens_2)}")