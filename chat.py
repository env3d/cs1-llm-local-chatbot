from llama_cpp import Llama
import random
import math
import sys, os


# Suppress stderr temporarily
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

llm = Llama(
      model_path="./qwen2.5-0.5b-instruct-q2_k.gguf",
      # n_gpu_layers=-1, # Uncomment to use GPU acceleration
      seed=random.randint(0, 2**31-1),
      #n_ctx=32768, # Uncomment to increase the context window
      verbose=False,
      logits_all=True
)

sys.stderr = stderr  # Restore stderr


def complete(prompt, temperature=0.7, max_tokens=1024, top_p=0.9, top_k=40, stop=['\n','<|endoftext|>','<|im_end|>']):
    result = llm(prompt, 
                 max_tokens=max_tokens, 
                 temperature=temperature, 
                 top_p=top_p, top_k=top_k, 
                 stop=stop
                 )
    return result['choices'][0]['text'].strip()

def chat(prompt, temperature=0.7, max_tokens=1024, top_p=0.9, top_k=40):
    if type(prompt) is not list:
        prompt = [{"role": "user", "content": prompt}]
    result = llm.create_chat_completion(prompt, 
                                        max_tokens=max_tokens, 
                                        temperature=temperature, 
                                        top_p=top_p, 
                                        top_k=top_k)
    return result['choices'][0]['message']['content'].strip()

def get_top_tokens(prompt, n=10):
    """
    Returns a list of the top n possible next tokens and their probabilities.
    """
    result = llm(
        prompt,
        max_tokens=1,
        temperature=0,      # Greedy, but returns logprobs for all options
        logprobs=n
    )
    logprobs = result['choices'][0]['logprobs']['top_logprobs'][0]
    # logprobs is a dict: {token: logprob}
    tokens_probs = [
        (token, float(round(math.exp(logprob), 6)))  # Convert log-prob to prob
        for token, logprob in logprobs.items()
    ]
    return tokens_probs