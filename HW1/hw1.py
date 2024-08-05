import requests
import os
import psutil
from functools import wraps
# from collections import OrderedDict

def memory_usage_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        result = func(*args, **kwargs)
        mem_after = process.memory_info().rss
        print(f"Memory used by {func.__name__}: {mem_after - mem_before} bytes")
        return result
    return wrapper

@memory_usage_decorator
def fetch_url_mem(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return #res.content[:first_n] if first_n else res.content

fetch_url("http://ukr.net")