# OpenRouter API Client with Retry Logic and Exponential Backoff
import requests
import time
import random
import logging
from typing import Optional, Dict, Any, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('openrouter_client')

class OpenRouterClient:
    def __init__(self, api_key=None, max_retries=3, initial_delay=1.0, max_delay=60.0, timeout=30):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.timeout = timeout
        
        if not self.api_key:
            logger.warning("No OpenRouter API key provided")
        
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        
        logger.info(f"OpenRouterClient initialized with max_retries={max_retries}")
    
    def _exponential_backoff(self, retry_count, error=None):
        if retry_count < 0:
            retry_count = 0
        base_delay = min(self.initial_delay * (2 ** retry_count), self.max_delay)
        jitter = random.uniform(0, 0.1 * base_delay)
        delay = base_delay + jitter
        if error:
            logger.warning(f"Retry {retry_count + 1}/{self.max_retries} in {delay:.2f}s after error: {type(error).__name__}")
        else:
            logger.info(f"Retry {retry_count + 1}/{self.max_retries} in {delay:.2f}s")
        return delay
    
    def _is_retryable_error(self, error, response=None):
        if isinstance(error, (requests.ConnectionError, requests.Timeout)):
            return True
        if response and response.status_code >= 500:
            return True
        if response and response.status_code == 429:
            return True
        return False
    
    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                if attempt > 0:
                    logger.info(f"Request succeeded after {attempt} retries")
                return response
            except Exception as e:
                if self._is_retryable_error(e, response if 'response' in locals() else None):
                    if attempt < self.max_retries:
                        delay = self._exponential_backoff(attempt, e)
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(f"All {self.max_retries + 1} attempts failed")
                        return None
                else:
                    raise
    
    def generate_image(self, prompt, model="flux1-dev", size="1024x1024", **kwargs):
        endpoint = "/images/generate"
        payload = {"model": model, "prompt": prompt, "size": size, **kwargs}
        response = self._make_request("POST", endpoint, json=payload)
        if response:
            try:
                return response.json()
            except:
                return None
        return None
    
    def chat_completions(self, messages, model="llama3-1-70b-8192", temperature=0.7, max_tokens=1000, **kwargs):
        endpoint = "/chat/completions"
        payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens, **kwargs}
        response = self._make_request("POST", endpoint, json=payload)
        if response:
            try:
                return response.json()
            except:
                return None
        return None
    
    def health_check(self):
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

def openrouter_request(method, endpoint, **kwargs):
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        logger.error("OPENROUTER_API_KEY environment variable not set")
        return None
    client = OpenRouterClient(api_key=api_key)
    return client._make_request(method, endpoint, **kwargs)

__all__ = ['OpenRouterClient', 'openrouter_request']
