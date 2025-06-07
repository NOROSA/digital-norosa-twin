# agent/builder.py
"""RecruiterAgent usando DeepSeek a través del transport chat-completions."""

import os
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool
from agents.models import OpenAIChatCompletionModel   # ← OBJETO DEL SDK
from agent.cv_loader import load_cv

# 1. CV en memoria -----------------------------------------------------------------
_CV_TEXT = load_cv()

@function_tool
def search_cv(query: str) -> str:
    q = query.lower()
    hits = [l for l in _CV_TEXT.splitlines() if q in l.lower()]
    return "\n".join(hits[:20]) or "No se encontró información en el CV."

# 2. Cliente DeepSeek ---------------------------------------------------------------
client_ds = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
)

# 3. Modelo chat-completion explícito ----------------------------------------------
chat_model = OpenAIChatCompletionModel(  # ← siempre usa /chat/completions
    model="deepseek-chat",
    client=client_ds,
)

def build_agent() -> Agent:
    return Agent(
        name="RecruiterAgent",
        instructions=(
            "Eres un asistente experto en la trayectoria profesional de Norbert. "
            "Cuando necesites hechos concretos, llama a search_cv y responde de forma breve y profesional, con un humor amable e inteligente cuando proceda."
        ),
        tools=[search_cv],
        model=chat_model,            # ← pasamos el objeto, no un string
    )

# 4. Helper async ------------------------------------------------------------------
async def chat_async(message: str) -> str:
    return (await Runner.run(build_agent(), message)).final_output
