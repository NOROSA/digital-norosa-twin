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
# 1. Carga tu CV una sola vez
# ──────────────────────────────
_docs = load_cv()
_CV_TEXT = "\n".join(doc.content for doc in _docs)

@function_tool
def search_cv(query: str) -> str:
    """Devuelve hasta 20 líneas del CV relevantes para la consulta."""
    q = query.lower()
    hits = [line for line in _CV_TEXT.splitlines() if q in line.lower()]
    return "\n".join(hits[:20]) or "No se encontró información en el CV."

# ──────────────────────────────
# 2. Construye el agente
# ──────────────────────────────
def build_agent() -> Agent:
    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1"),
    )
    set_default_openai_client(client)

    recruiter = Agent(
        name="RecruiterAgent",
        instructions=(
            "Eres un asistente experto en la trayectoria profesional del usuario. "
            "Cuando necesites hechos concretos, llama a search_cv. "
            "Responde siempre de forma breve, honesta y profesional."
        ),
        tools=[search_cv],
        model="deepseek-chat",
    )
    return recruiter

# Helper síncrono para servicios que no sean async (p.ej. Telegram)
def chat_sync(message: str) -> str:
    return Runner.run_sync(build_agent(), message).final_output
