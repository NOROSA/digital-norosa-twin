# 🤖 Digital Twin - Telegram Bot Corregido y Actualizado
# Sintaxis CrewAI 2025 verificada y correcta

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
    """🤖 Digital Twin con CrewAI sintaxis 2025"""
    
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
        """Configurar IA con CrewAI - Sintaxis 2025 corregida"""
        try:
            print("🧠 CONFIGURANDO IA...")
            
            if not DEEPSEEK_API_KEY:
                print("❌ DEEPSEEK_API_KEY falta")
                return
            
            # Configurar variables de entorno para OpenAI compatible
            os.environ["OPENAI_API_KEY"] = DEEPSEEK_API_KEY
            os.environ["OPENAI_API_BASE"] = DEEPSEEK_BASE_URL
            
            self.use_ai = True
            print("🎯 IA CONFIGURADA")
            
        except Exception as e:
            print(f"💥 Error setup_ai: {e}")
            self.use_ai = False
    
    async def process_query(self, message: str) -> str:
        """Procesa consulta usando CrewAI"""
        print(f"🔍 Procesando: '{message}' - IA habilitada: {self.use_ai}")
        
        if self.use_ai:
            try:
                return await self.ai_response(message)
            except Exception as e:
                print(f"💥 ERROR CON IA: {e}")
                import traceback
                traceback.print_exc()
                return self.fallback_response(message)
        
        return self.simple_response(message)
    
    async def ai_response(self, message: str) -> str:
        """Respuesta usando CrewAI - Sintaxis 2025 verificada"""
        try:
            # Importar CrewAI con sintaxis correcta
            from crewai import Agent, Task, Crew, Process
            
            # Configurar LLM usando el patrón actualizado
            try:
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    model="deepseek-chat",
                    base_url=DEEPSEEK_BASE_URL,
                    api_key=DEEPSEEK_API_KEY,
                    temperature=0.7
                )
            except ImportError:
                # Fallback si no está disponible langchain_openai
                print("⚠️ langchain_openai no disponible, usando configuración básica")
                llm = None
            
            # Crear agente con sintaxis 2025
            agent = Agent(
                role="AI Expert & Tech Consultant",
                goal="Provide helpful, professional information about AI and technology",
                backstory=f"""You are {self.cv_data['name']}, a {self.cv_data['title']} 
                based in {self.cv_data['location']}.
                
                Your expertise includes: {', '.join(self.cv_data['skills'])}
                
                Current role: {self.cv_data['experience'][0]['role']} at {self.cv_data['experience'][0]['company']}
                
                You are knowledgeable, helpful, and professional. Always provide accurate information
                about AI, technology, and your professional background.""",
                verbose=True,
                allow_delegation=False,
                llm=llm  # Puede ser None y CrewAI usará el default
            )
            
            # Crear tarea con sintaxis 2025
            task = Task(
                description=f"""Respond to this user query: "{message}"
                
                Provide a helpful, professional response based on your expertise in AI and technology.
                Be conversational but informative. If asked about your background, use the information
                from your backstory.""",
                expected_output="A helpful, professional response to the user's query",
                agent=agent
            )
            
            # Crear y ejecutar crew con sintaxis 2025
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,  # Explícitamente especificar proceso
                verbose=True
            )
            
            # Ejecutar crew
            result = crew.kickoff()
            
            # Extraer resultado según la versión de CrewAI
            if hasattr(result, 'raw'):
                return str(result.raw)
            else:
                return str(result)
            
        except ImportError as e:
            print(f"❌ CrewAI no disponible: {e}")
            raise Exception("CrewAI no está instalado correctamente")
        except Exception as e:
            print(f"❌ Error en AI response: {e}")
            raise
    
    def fallback_response(self, message: str) -> str:
        """Respuesta fallback inteligente usando datos del CV"""
        msg_lower = message.lower()
        
        # Respuestas específicas sobre IA
        if any(word in msg_lower for word in ['ai', 'inteligencia artificial', 'machine learning', 'crewai', 'langgraph']):
            return f"""🧠 **Mi experiencia en IA:**

Como {self.cv_data['title']}, trabajo con tecnologías de vanguardia:

**🛠️ Stack tecnológico:**
• **Frameworks IA:** LangGraph, CrewAI, LangChain
• **APIs LLM:** OpenAI, Claude, DeepSeek
• **ML/DL:** TensorFlow, PyTorch, Scikit-learn
• **Cloud:** AWS, Azure, Google Cloud

**🚀 Proyecto destacado:**
*{self.cv_data['projects'][0]['name']}*
🔧 Tech Stack: {self.cv_data['projects'][0]['tech']}
📋 {self.cv_data['projects'][0]['description']}

**💼 Experiencia actual:**
{self.cv_data['experience'][0]['role']} en {self.cv_data['experience'][0]['company']}
🏆 {self.cv_data['experience'][0]['highlights']}

¿Hay algo específico sobre IA que te interese conocer?"""
        
        # Respuesta sobre DeepSeek específicamente
        if 'deepseek' in msg_lower:
            return f"""🤖 **Experiencia con DeepSeek:**

Como {self.cv_data['title']}, he trabajado con varios LLMs incluyendo DeepSeek:

**🔧 Integración técnica:**
• API integration con CrewAI
• Optimización de prompts
• Configuración multi-modelo
• Cost optimization strategies

**💡 Ventajas de DeepSeek:**
• Excelente relación calidad/precio
• Soporte para APIs OpenAI-compatible
• Rendimiento competitivo en tareas de código

¿Te interesa implementar DeepSeek en tu proyecto?"""
        
        return self.simple_response(message)
    
    def simple_response(self, message: str) -> str:
        """Respuestas básicas sin IA - mejoradas"""
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['hola', 'hello', 'hi', 'hey']):
            return f"""👋 **¡Hola! Soy {self.cv_data['name']}**

*{self.cv_data['bio']}*

🎯 **Especialización:**
• Sistemas IA empresariales y multi-agente
• Arquitectura de datos y MLOps
• Integración de LLMs y automatización

🛠️ **Tech Stack actual:**
{', '.join(self.cv_data['skills'][:8])}

📍 {self.cv_data['location']}
⚡ {self.cv_data['availability']}

**¿En qué puedo ayudarte hoy?**"""

        elif any(word in msg_lower for word in ['experiencia', 'skills', 'tecnología', 'trabajo']):
            return f"""💼 **Mi trayectoria profesional:**

**🚀 Rol actual:**
{self.cv_data['experience'][0]['role']} en *{self.cv_data['experience'][0]['company']}* ({self.cv_data['experience'][0]['years']})

🏆 **Logros destacados:**
{self.cv_data['experience'][0]['highlights']}

**📚 Experiencia previa:**
{self.cv_data['experience'][1]['role']} en *{self.cv_data['experience'][1]['company']}*
🎯 {self.cv_data['experience'][1]['highlights']}

**🛠️ Stack tecnológico:**
{', '.join(self.cv_data['skills'])}

¿Hay alguna tecnología específica que te interese?"""

        elif any(word in msg_lower for word in ['proyecto', 'portfolio', 'casos']):
            projects_text = "\n\n".join([
                f"**{i+1}. {proj['name']}**\n🛠️ *Tech:* {proj['tech']}\n📋 {proj['description']}"
                for i, proj in enumerate(self.cv_data['projects'])
            ])
            
            return f"""🚀 **Proyectos destacados:**

{projects_text}

**📊 Impacto cuantificado:**
• Sistemas que procesan 1M+ transacciones/día
• Plataformas que sirven a 50k+ usuarios activos
• Reducción de costos operativos del 40%
• Mejora en tiempo de respuesta del 60%

¿Te interesa conocer detalles técnicos de algún proyecto?"""

        elif any(word in msg_lower for word in ['disponible', 'contratar', 'contacto', 'colaborar']):
            return f"""📅 **Disponibilidad y colaboración:**

⚡ **Estado actual:** {self.cv_data['availability']}

**🎯 Servicios que ofrezco:**
• 🤖 Desarrollo de sistemas IA multi-agente
• 🔗 Integración de LLMs (GPT, Claude, DeepSeek)
• 🏗️ Arquitectura de datos y MLOps
• 💡 Consultoría en transformación digital IA

**📋 Para iniciar colaboración, compárteme:**
• 📧 Tu email de contacto
• 🏢 Empresa/proyecto
• 🎯 Descripción del desafío técnico
• ⚡ Tecnologías involucradas
• 📅 Timeline esperado

**⏱️ Garantía: Respuesta en menos de 24 horas**

¿En qué proyecto estás trabajando?"""

        elif any(word in msg_lower for word in ['precio', 'coste', 'tarifa', 'presupuesto']):
            return f"""💰 **Estructura de colaboración:**

Como {self.cv_data['title']}, ofrezco diferentes modalidades:

**🎯 Consultoría estratégica:**
• Auditoría de arquitectura IA
• Roadmap tecnológico
• Due diligence técnico

**🛠️ Desarrollo técnico:**
• Implementación de sistemas IA
• Integración de LLMs
• MLOps y automatización

**📋 Para presupuesto personalizado:**
• Describe el scope del proyecto
• Timeline y urgencia
• Recursos técnicos disponibles
• Complejidad estimada

Cada proyecto es único - prefiero discutir detalles antes de dar cifras.

¿Cuál es tu proyecto específico?"""

        else:
            return f"""🤖 **Soy {self.cv_data['name']}**
*{self.cv_data['title']}*

**🧠 Experto en:**
• Inteligencia Artificial y Machine Learning
• Sistemas multi-agente (CrewAI, LangGraph)
• Arquitectura de datos enterprise
• Integración de LLMs y automatización

**💬 Puedes preguntarme sobre:**
• 🔧 Experiencia técnica y proyectos
• 🚀 Tecnologías de IA y mejores prácticas
• 📅 Disponibilidad para colaboraciones
• 💡 Soluciones específicas a tus desafíos

**¿Qué aspecto específico te interesa explorar?**"""


class TelegramBot:
    """🤖 Bot de Telegram optimizado"""
    
    def __init__(self):
        print("🤖 Inicializando bot...")
        
        if not TELEGRAM_TOKEN:
            print("❌ TELEGRAM_TOKEN requerido")
            exit(1)
            
        self.digital_twin = SimpleDigitalTwin()
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()
        print("✅ Bot inicializado")
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("about", self.about_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando start mejorado"""
        cv = self.digital_twin.cv_data
        
        welcome = f"""🚀 **¡Bienvenido al Digital Twin de {cv['name']}!**

*{cv['bio']}*

📍 **Ubicación:** {cv['location']}
💼 **Rol actual:** {cv['title']}
⚡ **Estado:** {cv['availability']}

**🎯 Soy especialista en:**
• Sistemas IA empresariales y multi-agente
• LangGraph, CrewAI, integración de LLMs
• Arquitectura de datos y MLOps

**💬 Comandos disponibles:**
• `/help` - Ver todas las opciones
• `/about` - Conocer mi experiencia detallada

**¡Pregúntame cualquier cosa sobre IA y tecnología!** 🤖"""
        
        await update.message.reply_text(welcome, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando help mejorado"""
        help_text = """📋 **¿Cómo puedo ayudarte?**

**🔍 Temas de consulta:**
• 💻 **Experiencia técnica** - Skills, proyectos, tecnologías
• 🧠 **Inteligencia Artificial** - CrewAI, LangGraph, LLMs
• 🚀 **Casos de uso** - Proyectos reales, implementaciones
• 📅 **Colaboración** - Disponibilidad, servicios, presupuestos
• 🎯 **Soluciones específicas** - Tu desafío técnico particular

**💡 Ejemplos de preguntas:**
• "¿Qué experiencia tienes con CrewAI?"
• "¿Cómo integrarías DeepSeek en un sistema empresarial?"
• "Cuéntame sobre tus proyectos de IA"
• "¿Estás disponible para consultoría?"

**🤖 ¡Solo escribe tu pregunta en lenguaje natural!**"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando about con información detallada"""
        cv = self.digital_twin.cv_data
        
        about_text = f"""👨‍💻 **{cv['name']}**
*{cv['title']}*

**🏢 Experiencia profesional:**

**🚀 Actual:** {cv['experience'][0]['role']}
📍 {cv['experience'][0]['company']} ({cv['experience'][0]['years']})
🏆 {cv['experience'][0]['highlights']}

**📚 Anterior:** {cv['experience'][1]['role']}
📍 {cv['experience'][1]['company']} ({cv['experience'][1]['years']})
🎯 {cv['experience'][1]['highlights']}

**🛠️ Stack tecnológico:**
{', '.join(cv['skills'])}

**💡 Enfoque:**
Especializado en democratizar la IA empresarial mediante sistemas multi-agente inteligentes y arquitecturas escalables.

¿Quieres conocer algún aspecto específico?"""
        
        await update.message.reply_text(about_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de texto con mejor UX"""
        try:
            # Mostrar typing indicator
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action="typing"
            )
            
            # Procesar mensaje
            response = await self.digital_twin.process_query(update.message.text)
            
            # Dividir respuesta si es muy larga
            if len(response) > 4096:
                # Telegram tiene límite de 4096 caracteres
                parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
                for part in parts:
                    await update.message.reply_text(part, parse_mode='Markdown')
            else:
                await update.message.reply_text(response, parse_mode='Markdown')
            
            # Log para debug
            user = update.effective_user
            print(f"👤 {user.first_name} ({user.id}): {update.message.text[:100]}...")
            print(f"🤖 Respuesta enviada ({len(response)} chars)")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            
            # Mensaje de error amigable
            error_msg = """🤖 Disculpa, encontré un problema técnico.

**¿Puedes intentar:**
• Reformular tu pregunta
• Usar `/help` para ver opciones
• Contactar directamente si es urgente

*Estoy trabajando para solucionarlo.* 🔧"""
            
            await update.message.reply_text(error_msg, parse_mode='Markdown')
    
    async def cleanup_webhook(self):
        """Limpia webhooks previos"""
        try:
            print("🧹 Limpiando conexiones previas...")
            await self.app.bot.delete_webhook(drop_pending_updates=True)
            await asyncio.sleep(2)
            print("✅ Conexiones limpiadas")
        except Exception as e:
            print(f"⚠️ Error limpiando conexiones: {e}")
    
    def start_bot(self):
        """Inicia el bot con manejo robusto de errores"""
        try:
            print("🚀 INICIANDO TELEGRAM BOT...")
            
            # Limpiar conexiones previas
            asyncio.run(self.cleanup_webhook())
            
            # Iniciar polling con configuración optimizada
            print("🔄 Iniciando polling...")
            self.app.run_polling(
                drop_pending_updates=True,
                timeout=30,
                poll_interval=1.0,
                bootstrap_retries=5
            )
            
        except KeyboardInterrupt:
            print("👋 Bot detenido por usuario")
        except Exception as e:
            logger.error(f"Error crítico en bot: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    print("🚀 INICIANDO DIGITAL TWIN BOT...")
    
    try:
        bot = TelegramBot()
        bot.start_bot()
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        print("\n💡 Verifica:")
        print("• TELEGRAM_TOKEN configurado")
        print("• Dependencias instaladas: pip install python-telegram-bot crewai")
        print("• Python >= 3.10")
        exit(1)