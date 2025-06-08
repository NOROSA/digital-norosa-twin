"""
Guardrail stay-on-topic: bloquea mensajes que no traten del CV de Norbert.
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

from agent.client import client_ds  # ← importa SIN circularidad

# ── Mini-checker ───────────────────────────────────────────────────────────
class TopicVerdict(BaseModel):
    off_topic: bool
    reason: str

checker_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,
)

checker = Agent(
    name="TopicChecker",
    instructions=(
        "Devuelve JSON {off_topic: true/false, reason: str}. "
        "off_topic = true si el mensaje NO trata del CV de Norbert Rodríguez."
    ),
    output_type=TopicVerdict,
    model=checker_model,
)

# ── Guardrail ──────────────────────────────────────────────────────────────
@input_guardrail
async def stay_on_topic(ctx, agent: Agent, user_input: str | List[str]) -> GuardrailFunctionOutput:
    verdict = await Runner.run(checker, user_input, context=ctx.context)

    if verdict.final_output.off_topic:
        return GuardrailFunctionOutput(
            output_info=verdict.final_output,
            tripwire_triggered=True,
            fallback_response=(
                "Lo siento, solo puedo hablar sobre la trayectoria "
                "profesional de Norbert Rodríguez 🤖🚀"
            ),
        )

    return GuardrailFunctionOutput(
        output_info=verdict.final_output,
        tripwire_triggered=False,
    )
