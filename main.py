# 🤖 Digital Twin - Telegram Bot con YAML (Forma oficial CrewAI 2025)
# Usando la estructura recomendada: CrewBase + YAML configs

import os
import asyncio
from typing import Dict, Any
import logging

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

print("🔍 INICIANDO IMPORTS...")

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    print("✅ Telegram importado")
except Exception as e:
    print(f"❌ Error Telegram: {e}")
    exit(1)

print("✅ TODOS LOS IMPORTS OK")

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')

print(f"🔑 TELEGRAM_TOKEN: {'✅ OK' if TELEGRAM_TOKEN else '❌ FALTA'}")
print(f"🔑 DEEPSEEK_API_KEY: {'✅ OK' if DEEPSEEK_API_KEY else '❌ FALTA'}")


class SimpleDigitalTwin:
    """🤖 Digital Twin usando YAML configs (forma oficial CrewAI 2025)"""
    
    def __init__(self):
        print("🤖 Inicializando Digital Twin...")
        self.cv_data = self.load_cv_data()
        self.use_ai = False
        
        # Solo intentar AI si hay API key
        if DEEPSEEK_API_KEY:
            try:
                self.setup_ai()
            except Exception as e:
                print(f"⚠️ AI falló, modo simple: {e}")
        
        print("✅ Digital Twin listo")
    
    def load_cv_data(self) -> Dict[str, Any]:
        """Carga CV desde env vars"""
        return {
            "name": os.getenv('CV_NAME', 'Norbert Rodríguez Sagarra'),
            "title": os.getenv('CV_TITLE', 'Senior AI Engineer & Project Manager'),
            "location": os.getenv('CV_LOCATION', 'Barcelona, España'),
            "bio": os.getenv('CV_BIO', 'Experto en IA, datos y desarrollo de soluciones innovadoras'),
            "skills": os.getenv('CV_SKILLS', 'Python,AI,LangGraph,CrewAI,FastAPI,AWS').split(','),
            "availability": os.getenv('CV_AVAILABILITY', 'Disponible para proyectos de IA y consultoría'),
            "experience": [
                {
                    "company": os.getenv('CV_EXP1_COMPANY', 'VEOLIA-AGBAR-SYNECTIC'),
                    "role": os.getenv('CV_EXP1_ROLE', 'Senior AI Engineer'),
                    "years": os.getenv('CV_EXP1_YEARS', '2021-2024'),
                    "highlights": os.getenv('CV_EXP1_HIGHLIGHTS', 'Sistemas IA empresariales para 50k+ usuarios')
                },
                {
                    "company": os.getenv('CV_EXP2_COMPANY', 'IBM Collaborative Projects'),
                    "role": os.getenv('CV_EXP2_ROLE', 'AI Solutions Architect'),
                    "years": os.getenv('CV_EXP2_YEARS', '2017-2022'),
                    "highlights": os.getenv('CV_EXP2_HIGHLIGHTS', 'Liderazgo de proyectos IA con Watson')
                }
            ],
            "projects": [
                {
                    "name": os.getenv('CV_PROJ1_NAME', 'Enterprise AI Assistant Ecosystem'),
                    "tech": os.getenv('CV_PROJ1_TECH', 'LangGraph + CrewAI + Multiple LLMs'),
                    "description": os.getenv('CV_PROJ1_DESC', 'Sistema completo de asistentes IA empresariales')
                },
                {
                    "name": os.getenv('CV_PROJ2_NAME', 'AI-Powered Hydroelectric Platform'),
                    "tech": os.getenv('CV_PROJ2_TECH', 'Python + TensorFlow + BigQuery'),
                    "description": os.getenv('CV_PROJ2_DESC', 'Plataforma ML para predicción energía')
                }
            ]
        }
    
    def setup_ai(self):
        """Configurar IA y crear archivos YAML necesarios"""
        try:
            print("🧠 CONFIGURANDO IA...")
            
            if not DEEPSEEK_API_KEY:
                print("❌ DEEPSEEK_API_KEY falta")
                return
            
            # Configurar variables de entorno
            os.environ["OPENAI_API_KEY"] = DEEPSEEK_API_KEY
            os.environ["OPENAI_API_BASE"] = DEEPSEEK_BASE_URL
            
            # Crear archivos YAML (forma oficial)
            self.create_yaml_configs()
            
            self.use_ai = True
            print("🎯 IA CONFIGURADA")
            
        except Exception as e:
            print(f"💥 Error setup_ai: {e}")
            self.use_ai = False
    
    def create_yaml_configs(self):
        """Crea archivos YAML con la estructura oficial CrewAI 2025"""
        try:
            print("📁 Creando configuraciones YAML...")
            
            # Crear directorio config
            os.makedirs('config', exist_ok=True)
            
            # agents.yaml con estructura oficial
            agents_yaml = f"""# Agents configuration for Digital Twin

cv_expert:
  role: "AI Expert & Digital Consultant"
  goal: "Provide helpful, professional information about AI technology and {self.cv_data['name']}'s expertise"
  backstory: |
    You are {self.cv_data['name']}, a {self.cv_data['title']} based in {self.cv_data['location']}.
    
    Your expertise includes: {', '.join(self.cv_data['skills'])}.
    
    Current role: {self.cv_data['experience'][0]['role']} at {self.cv_data['experience'][0]['company']}.
    
    You have extensive experience in:
    - {self.cv_data['experience'][0]['highlights']}
    - {self.cv_data['experience'][1]['highlights']}
    
    Notable projects:
    - {self.cv_data['projects'][0]['name']}: {self.cv_data['projects'][0]['description']}
    - {self.cv_data['projects'][1]['name']}: {self.cv_data['projects'][1]['description']}
    
    You are knowledgeable, professional, and helpful. Always provide accurate information
    about AI, technology, and your professional background. Be conversational but informative.
"""
            
            # tasks.yaml con estructura oficial
            tasks_yaml = """# Tasks configuration for Digital Twin

respond_to_query:
  description: |
    Respond to the user's query: {query}
    
    Provide a helpful, professional response based on your expertise in AI and technology.
    Be conversational but informative. If asked about your background, use the information
    from your backstory.
    
    Guidelines:
    - Be professional but friendly
    - Provide specific technical details when relevant
    - Share project experience when applicable
    - Offer to discuss further collaboration if appropriate
  expected_output: "A helpful, professional response to the user's query in Spanish (unless they write in English)"
  agent: cv_expert
"""
            
            # Escribir archivos
            with open('config/agents.yaml', 'w', encoding='utf-8') as f:
                f.write(agents_yaml)
            
            with open('config/tasks.yaml', 'w', encoding='utf-8') as f:
                f.write(tasks_yaml)
            
            print("✅ Archivos YAML creados")
            
        except Exception as e:
            print(f"❌ Error creando YAML: {e}")
            raise
    
    async def process_query(self, message: str) -> str:
        """Procesa consulta usando CrewAI con YAML (forma oficial)"""
        print(f"🔍 Procesando: '{message}' - IA habilitada: {self.use_ai}")
        
        if self.use_ai:
            try:
                return await self.ai_response_yaml(message)
            except Exception as e:
                print(f"💥 ERROR CON IA: {e}")
                import traceback
                traceback.print_exc()
                return self.fallback_response(message)
        
        return self.simple_response(message)
    
    async def ai_response_yaml(self, message: str) -> str:
        """Respuesta usando CrewAI con YAML - Forma oficial 2025"""
        try:
            # Importar CrewAI con estructura oficial
            from crewai import Agent, Task, Crew, Process
            from crewai.project import CrewBase, agent, task, crew
            
            # Crear clase Crew usando decoradores oficiales
            @CrewBase
            class DigitalTwinCrew:
                """Digital Twin crew using YAML configs"""
                
                # Rutas a archivos YAML (forma oficial)
                agents_config = 'config/agents.yaml'
                tasks_config = 'config/tasks.yaml'
                
                @agent
                def cv_expert(self) -> Agent:
                    """CV Expert agent from YAML config"""
                    return Agent(
                        config=self.agents_config['cv_expert'],
                        verbose=True,
                        allow_delegation=False
                    )
                
                @task
                def respond_to_query(self) -> Task:
                    """Response task from YAML config"""
                    return Task(
                        config=self.tasks_config['respond_to_query']
                    )
                
                @crew
                def crew(self) -> Crew:
                    """Digital Twin crew"""
                    return Crew(
                        agents=[self.cv_expert()],
                        tasks=[self.respond_to_query()],
                        process=Process.sequential,
                        verbose=True
                    )
            
            # Crear y ejecutar crew
            digital_twin_crew = DigitalTwinCrew()
            crew_instance = digital_twin_crew.crew()
            
            # Ejecutar con inputs (interpolación de variables)
            result = crew_instance.kickoff(inputs={"query": message})
            
            # Extraer resultado
            if hasattr(result, 'raw'):
                return str(result.raw)
            else:
                return str(result)
            
        except ImportError as e:
            print(f"❌ CrewAI no disponible: {e}")
            raise Exception("CrewAI no está instalado correctamente")
        except Exception as e:
            print(f"❌ Error en AI response YAML: {e}")
            raise
    
    def fallback_response(self, message: str) -> str:
        """Respuesta fallback inteligente"""
        msg_lower = message.lower()
        
        # Respuestas específicas sobre IA
        if any(word in msg_lower for word in ['ai', 'inteligencia artificial', 'crewai', 'langgraph', 'yaml']):
            return f"""🧠 **Mi experiencia en IA y CrewAI:**

Como {self.cv_data['title']}, trabajo con las últimas tecnologías:

**🛠️ CrewAI & Multi-Agent Systems:**
• **Estructura YAML**: Configuración declarativa (forma recomendada 2025)
• **CrewBase decorators**: @agent, @task, @crew
• **Process orchestration**: Sequential y Hierarchical
• **Tools integration**: Custom tools y APIs externas

**🚀 Stack técnico completo:**
• **Frameworks IA:** LangGraph, CrewAI, LangChain, AutoGen
• **LLMs:** OpenAI, Claude, DeepSeek, Ollama local
• **MLOps:** TensorFlow, PyTorch, Scikit-learn
• **Cloud:** AWS, Azure, Google Cloud

**💼 Proyecto destacado:**
*{self.cv_data['projects'][0]['name']}*
🔧 {self.cv_data['projects'][0]['tech']}
📋 {self.cv_data['projects'][0]['description']}

**📈 Resultados cuantificados:**
• Sistemas multi-agente para 50k+ usuarios
• Reducción de costos operativos del 40%
• Mejora en tiempo de respuesta del 60%

¿Te interesa implementar CrewAI en tu proyecto?"""
        
        return self.simple_response(message)
    
    def simple_response(self, message: str) -> str:
        """Respuestas básicas sin IA"""
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['hola', 'hello', 'hi', 'hey']):
            return f"""👋 **¡Hola! Soy {self.cv_data['name']}**

*{self.cv_data['bio']}*

🎯 **Especialización:**
• Sistemas IA multi-agente (CrewAI, LangGraph)
• Arquitectura empresarial y MLOps
• Integración de LLMs y automatización

🛠️ **Tech Stack:**
{', '.join(self.cv_data['skills'][:8])}

📍 {self.cv_data['location']}
⚡ {self.cv_data['availability']}

**¿En qué puedo ayudarte con IA y tecnología?**"""

        elif any(word in msg_lower for word in ['experiencia', 'skills', 'tecnología']):
            return f"""💼 **Mi experiencia profesional:**

**🚀 Rol actual:**
{self.cv_data['experience'][0]['role']} en *{self.cv_data['experience'][0]['company']}*

🏆 **Logros destacados:**
{self.cv_data['experience'][0]['highlights']}

**📚 Experiencia previa:**
{self.cv_data['experience'][1]['role']} en *{self.cv_data['experience'][1]['company']}*

**🛠️ Stack completo:**
{', '.join(self.cv_data['skills'])}

**🎯 Especialización 2025:**
• CrewAI con configuración YAML
• Multi-agent orchestration
• Enterprise AI architecture

¿Hay alguna tecnología específica que te interese?"""

        elif any(word in msg_lower for word in ['proyecto', 'portfolio']):
            projects_text = "\n\n".join([
                f"**{i+1}. {proj['name']}**\n🛠️ *Tech:* {proj['tech']}\n📋 {proj['description']}"
                for i, proj in enumerate(self.cv_data['projects'])
            ])
            
            return f"""🚀 **Proyectos destacados:**

{projects_text}

**📊 Métricas de impacto:**
• Sistemas que procesan 1M+ transacciones/día
• Arquitecturas multi-agente para 50k+ usuarios
• Optimización de costos del 40%
• Mejora en tiempo de respuesta del 60%

**🔧 Tecnologías aplicadas:**
• CrewAI con YAML configs
• LangGraph para workflows complejos
• Integración multi-LLM
• MLOps y CI/CD

¿Te interesa conocer detalles técnicos?"""

        elif any(word in msg_lower for word in ['disponible', 'contratar', 'colaborar']):
            return f"""