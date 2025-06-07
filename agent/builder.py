"""RecruiterAgent — DeepSeek a través de OpenAI-Agents (chat-completions)."""

import os
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    function_tool,
    OpenAIChatCompletionsModel,   # ← nombre EXACTO del SDK 0.0.17
)
from agent.cv_loader import load_cv

# 1 ── Metemos TODO tu CV en memoria (sin cortes)
CV_TEXT = load_cv()

# 2 ── Cliente DeepSeek ------------------------------------------------------
client_ds = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
)

# 3 ── Modelo chat-completions explícito (usa /chat/completions) ------------
chat_model = OpenAIChatCompletionsModel(      # ✅ plural + param correcto
    model="deepseek-chat",
    openai_client=client_ds,
)

# 4 ── Agente ---------------------------------------------------------------
def build_agent() -> Agent:
    return Agent(
        name="RecruiterAgent",
        instructions=(
            "Eres un asistente experto en la trayectoria profesional de Norbert. "
            "Solo usa la información del siguiente CV cuando respondas.\n\n"
            f"{CV_TEXT}\n\n"
            "— Fin del CV —\n"
            "Responde de forma breve, honesta y profesional."
        ),
        model=chat_model,
    )

# 5 ── Helper async para Telegram ------------------------------------------
async def chat_async(message: str) -> str:
    result = await Runner.run(build_agent(), message)
    return result.final_output
