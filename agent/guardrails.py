"""Guardrail stay-on-topic: NorosAI solo responde a preguntas sobre el CV."""

from __future__ import annotations
from typing import List

from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    input_guardrail,
    OpenAIChatCompletionsModel,
)
from agent.client import client_ds  # Cliente DeepSeek compartido

# ── Mini-checker que devuelve 'OK' o 'OFF' ────────────────────────────────
checker_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,
)

checker = Agent(
    name="TopicChecker",
    instructions=(
        "Si la frase trata sobre la trayectoria profesional de Norbert "
        "Rodríguez responde exactamente 'OK'.\n"
        "Si no, responde exactamente 'OFF'.\n"
        "No añadas nada más."
    ),
    model=checker_model,
)

# ── Guardrail ─────────────────────────────────────────────────────────────
@input_guardrail
async def stay_on_topic(ctx, agent: Agent, user_input: str | List[str]) -> GuardrailFunctionOutput:
    verdict_raw = await Runner.run(checker, user_input, context=ctx.context)
    verdict = verdict_raw.final_output.strip().upper()

    if verdict == "OFF":
        return GuardrailFunctionOutput(
            output_info=verdict,
            tripwire_triggered=True,
            fallback_response=(
                "Lo siento, solo puedo hablar sobre la trayectoria "
                "profesional de Norbert Rodríguez 🤖🚀"
            ),
        )

    # Si verdict == 'OK' o cualquier otra cosa, seguimos
    return GuardrailFunctionOutput(
        output_info=verdict,
        tripwire_triggered=False,
    )
