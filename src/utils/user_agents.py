from fake_useragent import UserAgent

def get_random_user_agent():
    """Generate random user agent"""
    ua = UserAgent()
    return ua.random

def get_common_user_agents():
    """Return list of common user agents"""
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]