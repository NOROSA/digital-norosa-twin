"""RecruiterAgent — DeepSeek a través de OpenAI-Agents (chat-completions)."""

import os
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    function_tool,
    OpenAIChatCompletionsModel,
)
from agent.cv_loader import load_cv
from agent.guardrails import stay_on_topic        # ← NUEVO

# 1 ── Carga TODO el CV en memoria
CV_TEXT = load_cv()

# 2 ── Cliente DeepSeek
client_ds = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
)

# 3 ── Modelo chat-completions
chat_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,
)

# 4 ── Construcción del agente con rail
def build_agent() -> Agent:
    return Agent(
        name="RecruiterAgent",
        instructions=(
            "¡Hola! Soy **NorosAI** 🤖, un robot con chispa especializado en la carrera de Norbert Rodríguez. "
            "Respondo con humor ligero y profesionalidad. "
            "Solo utilizo la información del CV de Norbert; si no sé algo, lo admito sin inventar. "
            "Suelto algún emoji simpático (🤖🚀) para humanizarme.\n\n"
            "===== CURRICULUM VITAE =====\n"
            f"{CV_TEXT}\n"
            "===== FIN DEL CV ====="
        ),
        model=chat_model,
        input_guardrails=[stay_on_topic],   # ← rail activo
    )

# 5 ── Helper async para Telegram
async def chat_async(message: str) -> str:
    result = await Runner.run(build_agent(), message)
    return result.final_output
