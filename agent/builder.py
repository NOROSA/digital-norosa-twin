"""RecruiterAgent — DeepSeek vía OpenAI-Agents (chat-completions)."""

import os
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
)
from agent.cv_loader import load_cv
from agent.guardrails import stay_on_topic
from agent.client import client_ds          # ← ya no hay circularidad

# 1. CV completo
CV_TEXT = load_cv()

# 2. Modelo chat-completions
chat_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,
)

# 3. Agente con guardrail
def build_agent() -> Agent:
    return Agent(
        name="RecruiterAgent",
        instructions=(
            "¡Hola! Soy **NorosAI** 🤖, un robot con chispa especializado en la carrera de Norbert Rodríguez. "
            "Respondo con humor y profesionalidad; solo uso la información del CV y si no sé algo lo admito. "
            "🤖🚀\n\n"
            "===== CURRICULUM VITAE =====\n"
            f"{CV_TEXT}\n"
            "===== FIN DEL CV ====="
        ),
        model=chat_model,
        input_guardrails=[stay_on_topic],
    )

# 4. Helper async
async def chat_async(message: str) -> str:
    result = await Runner.run(build_agent(), message)
    return result.final_output
