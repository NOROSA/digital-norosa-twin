import os
import openai
from openai_agents import AgentBuilder, DocumentSearchTool
from agent.cv_loader import load_cv


def build_agent():
    # Configura el SDK para DeepSeek
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.base_url = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")

    # 1) Carga tu CV y créa un DocumentSearchTool muy simple
    documents = load_cv()  # -> [Document(...), ...]
    search_tool = DocumentSearchTool.from_documents(
        documents,
        name="Curriculum",
        description="Busca datos concretos sobre la carrera del usuario"
    )

    # 2) Monta el agente
    builder = AgentBuilder(
        name="RecruiterAgent",
        llm_model="deepseek-chat",  # Cambia si usas otro
        description="Asistente que responde dudas sobre la trayectoria profesional del usuario."
    )
    builder.add_tool(search_tool)
    builder.set_system_prompt(
        "Eres un asistente experto en la trayectoria profesional de tu usuario. "
        "Usa exclusivamente la información del Curriculum para responder de forma breve, honesta y profesional. "
        "Si no sabes algo, reconoce tu desconocimiento."
    )

    return builder.build()