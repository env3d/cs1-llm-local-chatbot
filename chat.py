import random
import math
import sys, os

# Detect if we're running inside a testrunner and skip heavy model init
running_under_testrunner = (
    os.environ.get("TESTRUNNER", "").lower() in ("1", "true", "yes")
    or "PYTEST_CURRENT_TEST" in os.environ
)

llm = None
if not running_under_testrunner:
    from llama_cpp import Llama
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
    if llm is None:
        raise RuntimeError("LLM not initialized (running under testrunner).")
    
    result = llm(prompt, 
                 max_tokens=max_tokens, 
                 temperature=temperature, 
                 top_p=top_p, top_k=top_k, 
                 stop=stop
                 )
    return result['choices'][0]['text'].strip()

def chat(prompt, temperature=0.7, max_tokens=1024, top_p=0.9, top_k=40):
    if llm is None:
        raise RuntimeError("LLM not initialized (running under testrunner).")
    
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
    if llm is None:
        raise RuntimeError("LLM not initialized (running under testrunner).")
    
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