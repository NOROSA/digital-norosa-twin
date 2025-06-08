"""Guardrail: impide que NorosAI hable de temas fuera del CV de Norbert."""

from __future__ import annotations
from typing import List

from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    input_guardrail,
    OpenAIChatCompletionsModel,
)
from agent.client import client_ds  # cliente DeepSeek compartido


# ── 1. Mini-checker “OK / OFF” ───────────────────────────────────────────
checker_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,
)

checker = Agent(
    name="TopicChecker",
    instructions=(
        "Responde SOLO «OK» si el mensaje trata de la trayectoria "
        "profesional de Norbert Rodríguez.\n"
        "Responde SOLO «OFF» en cualquier otro caso."
    ),
    model=checker_model,
)


# ── 2. Guardrail propiamente dicho ───────────────────────────────────────
@input_guardrail
async def stay_on_topic(ctx, agent: Agent, user_input: str | List[str]) -> GuardrailFunctionOutput:
    verdict_raw = await Runner.run(checker, user_input, context=ctx.context)
    verdict = verdict_raw.final_output.strip().upper()

    if verdict == "OFF":
        return GuardrailFunctionOutput(
            output_info="OFF",
            tripwire_triggered=True,
            assistant_response_override=(
                "Lo siento, solo puedo hablar sobre la trayectoria "
                "profesional de Norbert Rodríguez 🤖🚀"
            ),
        )

    return GuardrailFunctionOutput(
        output_info="OK",
        tripwire_triggered=False,
    )
