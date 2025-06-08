"""
Guardrail stay-on-topic:
   - Detecta mensajes que NO tratan del CV de Norbert
   - Si se salen de tema, devuelve un mensaje estándar.
"""

from __future__ import annotations
from typing import List

from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    input_guardrail,
    OpenAIChatCompletionsModel,
)
from agent.client import client_ds   # cliente DeepSeek

# ── mini-checker que responde “OK” o “OFF” ────────────────────────────────
checker_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,
)

checker = Agent(
    name="TopicChecker",
    instructions=(
        "Responde únicamente 'OK' si la entrada SE RELACIONA con la "
        "trayectoria profesional de Norbert Rodríguez.\n"
        "Responde únicamente 'OFF' si no está relacionada."
    ),
    model=checker_model,
)


# ── guardrail propiamente dicho ────────────────────────────────────────────
@input_guardrail
async def stay_on_topic(ctx, agent: Agent, user_input: str | List[str]) -> GuardrailFunctionOutput:
    verdict_raw = await Runner.run(checker, user_input, context=ctx.context)
    verdict = verdict_raw.final_output.strip().upper()

    if verdict == "OFF":
        return GuardrailFunctionOutput(
            output_info="OFF",
            tripwire_triggered=True,
            assistant_response=(
                "Lo siento, solo puedo hablar sobre la trayectoria "
                "profesional de Norbert Rodríguez 🤖🚀"
            ),
        )

    # Si verdict == 'OK' -> continúa flujo normal
    return GuardrailFunctionOutput(
        output_info="OK",
        tripwire_triggered=False,
    )
