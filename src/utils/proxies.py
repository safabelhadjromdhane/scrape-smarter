import random
import requests

PROXY_LIST = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080"
]

def get_random_proxy():
    """Return a random proxy from the list"""
    return {"http": random.choice(PROXY_LIST), "https": random.choice(PROXY_LIST)}

def is_proxy_working(proxy):
    """Check if proxy is working"""
    try:
        requests.get("http://example.com", proxies=proxy, timeout=5)
        return True
    except:
        return False