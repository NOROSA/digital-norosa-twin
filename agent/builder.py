"""Construye y expone el RecruiterAgent basado en el SDK oficial `openai-agents`."""

import os
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_client,
)
from agent.cv_loader import load_cv

# ──────────────────────────────
# 1. Carga el CV en memoria
# ──────────────────────────────
_CV_TEXT = load_cv()


@function_tool
def search_cv(query: str) -> str:
    """Devuelve las primeras 20 líneas del CV que contengan la consulta."""
    q = query.lower()
    hits = [line for line in _CV_TEXT.splitlines() if q in line.lower()]
    return "\n".join(hits[:20]) or "No se encontró información en el CV."


# ──────────────────────────────
# 2. Construye el agente
# ──────────────────────────────
def build_agent() -> Agent:
    """Devuelve el agente listo para usar con DeepSeek como backend."""
    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1"),
    )
    set_default_openai_client(client)

    return Agent(
        name="RecruiterAgent",
        instructions=(
            "Eres un asistente experto en la trayectoria profesional de Norbert. "
            "Cuando necesites hechos concretos, llama a search_cv y responde de forma breve y profesional."
        ),
        tools=[search_cv],
        model="deepseek-chat",
    )


# ──────────────────────────────
# 3. Helper asíncrono para Telegram
# ──────────────────────────────
async def chat_async(message: str) -> str:
    """Obtiene la respuesta del agente de forma asíncrona (compatible con Telegram)."""
    return (await Runner.run(build_agent(), message)).final_output
