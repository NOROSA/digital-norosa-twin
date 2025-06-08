"""Cliente(s) OpenAI-compatible compartidos por todo el proyecto."""

import os
from openai import AsyncOpenAI

# DeepSeek
client_ds = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
)
