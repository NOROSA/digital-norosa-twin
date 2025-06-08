# agent/guardrails.py  (sustituye el bloque del checker)

from agent.client import client_ds          # cliente DeepSeek compartido
from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    input_guardrail,
    OpenAIChatCompletionsModel,
)
from pydantic import BaseModel
from typing import List

class TopicVerdict(BaseModel):
    off_topic: bool
    reason: str

checker_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client_ds,
    response_format={"type": "json_object"},    # 👈 forzamos json_object
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
