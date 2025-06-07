"""RecruiterAgent — DeepSeek vía OpenAI-Agents (chat completions)."""

import os
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel  # ← S en “Completions”
from agent.cv_loader import load_cv

# ──────────────────────────────
# 1. CV cargado en memoria
# ──────────────────────────────
_CV_TEXT = load_cv()


@function_tool
def search_cv(query: str) -> str:
    """Devuelve hasta 20 líneas del CV que contengan el término de búsqueda."""
    q = query.lower()
    hits = [line for line in _CV_TEXT.splitlines() if q in line.lower()]
    return "\n".join(hits[:20]) or "No se encontró información en el CV."


# ──────────────────────────────
# 2. Cliente DeepSeek y modelo chat-completions
# ──────────────────────────────
client_ds = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
)

chat_model = OpenAIChatCompletionsModel(       # ← modelo correcto
    model="deepseek-chat",
    openai_client=client_ds,                   # parámetro del SDK
)

# ──────────────────────────────
# 3. Construcción del agente
# ──────────────────────────────
def build_agent() -> Agent:
    return Agent(
        name="RecruiterAgent",
        instructions=(
            "Eres un asistente experto en la trayectoria profesional de Norbert. "
            "Cuando necesites datos concretos, llama a search_cv y responde de forma breve y profesional."
        ),
        tools=[search_cv],
        model=chat_model,
    )


# ──────────────────────────────
# 4. Helper asíncrono (Telegram)
# ──────────────────────────────
async def chat_async(message: str) -> str:
    result = await Runner.run(build_agent(), message)
    return result.final_output
