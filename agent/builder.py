"""Construye y expone el RecruiterAgent basado en el SDK oficial `openai-agents`."""

import os
from openai import AsyncOpenAI
# El SDK (v 0.0.17) expone sus clases en el paquete de nivel superior `agents`
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
            "Eres un asistente experto en la trayectoria profesional del usuario. "
            "Cuando necesites hechos concretos, llama a search_cv. "
            "Responde siempre de forma breve, honesta y profesional."
        ),
        tools=[search_cv],
        model="deepseek-chat",
    )

# Helper síncrono para integraciones no-async (Telegram)
def chat_sync(message: str) -> str:
    return Runner.run_sync(build_agent(), message).final_output
