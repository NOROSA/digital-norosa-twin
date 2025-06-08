"""
Guardrail stay-on-topic: bloquea entradas que no traten del CV de Norbert.
"""

from __future__ import annotations
from typing import List

from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    input_guardrail,
    OpenAIChatCompletionsModel,
)

# ── 1. Cliente DeepSeek que ya creaste en builder.py ───────────────────────
from agent.builder import client_ds  # importa el cliente compartido

# ── 2. Mini-checker que decide si la entrada es on-topic ───────────────────
class TopicVerdict(BaseModel):
    off_topic: bool
    reason: str

checker_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,     # ⚠️ parámetro correcto
)

checker = Agent(
    name="TopicChecker",
    instructions=(
        "Devuelve JSON {off_topic: true/false, reason: str}. "
        "off_topic es true si el mensaje NO pide información sobre "
        "la trayectoria profesional de Norbert Rodríguez."
    ),
    output_type=TopicVerdict,
    model=checker_model,
)

# ── 3. Guardrail propiamente dicho ─────────────────────────────────────────
@input_guardrail
async def stay_on_topic(
    ctx,                           # RunContextWrapper implícito
    agent: Agent,
    user_input: str | List[str],
) -> GuardrailFunctionOutput:
    verdict = await Runner.run(checker, user_input, context=ctx.context)
    if verdict.final_output.off_topic:
        # Tripwire + respuesta de fallback (para que no lance excepción)
        return GuardrailFunctionOutput(
            output_info=verdict.final_output,
            tripwire_triggered=True,
            fallback_response=(
                "Lo siento, solo puedo hablar sobre la trayectoria "
                "profesional de Norbert Rodríguez 🤖🚀"
            ),
        )
    # Si está en tema, seguimos normal
    return GuardrailFunctionOutput(
        output_info=verdict.final_output,
        tripwire_triggered=False,
    )
