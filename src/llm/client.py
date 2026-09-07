import time
import random
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from src.config import settings
from src.llm.usage import track_usage

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def call_llm(system_prompt: str, user_content: str, model: str = settings.DEFAULT_MODEL, temperature: float = settings.DEFAULT_TEMPERATURE, stage: str = "general") -> str:
    max_retries = 5
    base_delay = 1.0

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                timeout=settings.REQUEST_TIMEOUT
            )
            
            usage = response.usage
            if usage:
                track_usage(stage, model, usage.prompt_tokens, usage.completion_tokens)
                
            return response.choices[0].message.content

        except (RateLimitError, APIConnectionError, APITimeoutError) as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"LLM call failed after {max_retries} attempts: {e}")
            
            sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
            time.sleep(sleep_time)
        except Exception as e:
            raise RuntimeError(f"Non-recoverable LLM error: {e}")