# agent/guardrails.py
from agents import (
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    Runner,
    Agent,
    RunContextWrapper,
)
from pydantic import BaseModel

# 1) Un agente mini-checker que decide si el mensaje está fuera de tema
class TopicCheck(BaseModel):
    off_topic: bool
    reason: str

topic_checker = Agent(
    name="Topic checker",
    instructions=(
        "Devuelve JSON {off_topic: true/false, reason: …}. "
        "off_topic debe ser true si la entrada NO trata del CV de Norbert Rodríguez."
    ),
    output_type=TopicCheck,
)

# 2) Nuestro guardrail
@input_guardrail
async def on_topic_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    user_input: str | list,
) -> GuardrailFunctionOutput:
    result = await Runner.run(topic_checker, user_input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.off_topic,   # ← dispara si es off-topic
    )
