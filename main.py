# 🤖 Digital Twin - VERSIÓN PURA COMO ASUKA
# Solo Telegram Bot, sin FastAPI ni complicaciones

import os
import asyncio
from typing import Dict, Any

print("🔍 INICIANDO IMPORTS...")

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
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
    """🤖 Versión simple como Asuka"""
    
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
        """Configurar IA si es posible"""
        try:
            print("🧠 Configurando IA...")
            
            os.environ["OPENAI_API_KEY"] = DEEPSEEK_API_KEY
            os.environ["OPENAI_API_BASE"] = DEEPSEEK_BASE_URL
            
            from crewai import Agent, Task
            
            self.agent = Agent(
                role='AI Assistant',
                goal='Help users professionally',
                backstory=f'You are {self.cv_data["name"]}, an AI expert.',
                verbose=False,
                allow_delegation=False
            )
            
            self.use_ai = True
            print("✅ IA configurada")
            
        except Exception as e:
            print(f"⚠️ IA falló: {e}")
            self.use_ai = False
    
    async def process_query(self, message: str) -> str:
        """Procesa consulta"""
        
        if self.use_ai:
            try:
                print(f"🧠 Procesando con IA: {message[:50]}...")
                
                from crewai import Crew, Task
                
                task = Task(
                    description=f'Respond professionally as {self.cv_data["name"]}: {message}',
                    agent=self.agent,
                    expected_output='Professional response'
                )
                
                crew = Crew(agents=[self.agent], tasks=[task], verbose=False)
                result = crew.kickoff()
                
                response = str(result)
                print(f"✅ IA respondió: {len(response)} chars")
                return response
                
            except Exception as e:
                print(f"❌ Error IA específico: {e}")
                print(f"❌ Tipo de error: {type(e).__name__}")
                # Fallback mejorado
                return self.ai_fallback_response(message)
        
        # Fallback sin IA
        print("🔄 Usando respuesta simple (sin IA)")
        return self.simple_response(message)
    
    def ai_fallback_response(self, message: str) -> str:
        """Respuesta inteligente sin IA pero usando datos del CV"""
        msg_lower = message.lower()
        
        # Respuestas más específicas sobre IA/OpenAI
        if any(word in msg_lower for word in ['openai', 'gpt', 'ai', 'inteligencia artificial']):
            return f"""🧠 **Mi experiencia en IA:**

Como {self.cv_data['title']}, tengo amplia experiencia con:

**🛠️ Tecnologías IA:**
• LangGraph, CrewAI, OpenAI API
• LangChain, AutoGen, HuggingFace  
• GPT-4, Claude, DeepSeek

**🚀 Proyectos recientes:**
• {self.cv_data['projects'][0]['name']} - {self.cv_data['projects'][0]['description']}

**💼 Experiencia actual:**
{self.cv_data['experience'][0]['role']} en {self.cv_data['experience'][0]['company']}

¿Te interesa algún aspecto específico de IA?"""
        
        # Usar respuesta simple por defecto
        return self.simple_response(message)
    
    def simple_response(self, message: str) -> str:
        """Respuestas sin IA - MEJORADAS"""
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['hola', 'hello', 'hi']):
            return f"""👋 ¡Hola! Soy {self.cv_data['name']}, {self.cv_data['title']}.

{self.cv_data['bio']}

🚀 **Especialidades:**
• Sistemas IA empresariales
• LangGraph, CrewAI, OpenAI API  
• Arquitectura de datos y MLOps

¿En qué puedo ayudarte?"""

        elif any(word in msg_lower for word in ['experiencia', 'skills', 'tecnolog']):
            return f"""🛠️ **Mi experiencia técnica:**

**🎯 Skills principales:** 
{', '.join(self.cv_data['skills'][:8])}... y más

**💼 Experiencia actual:**
{self.cv_data['experience'][0]['role']} en {self.cv_data['experience'][0]['company']} ({self.cv_data['experience'][0]['years']})

**🏆 Logros destacados:**
{self.cv_data['experience'][0]['highlights']}

**📚 Experiencia previa:**
{self.cv_data['experience'][1]['role']} en {self.cv_data['experience'][1]['company']}

¿Hay alguna tecnología específica que te interese?"""

        elif any(word in msg_lower for word in ['proyecto', 'portfolio']):
            return f"""🚀 **Proyectos destacados:**

**1. {self.cv_data['projects'][0]['name']}**
🛠️ Tech: {self.cv_data['projects'][0]['tech']}
📋 {self.cv_data['projects'][0]['description']}

**2. {self.cv_data['projects'][1]['name']}**  
🛠️ Tech: {self.cv_data['projects'][1]['tech']}
📋 {self.cv_data['projects'][1]['description']}

💡 He trabajado en sistemas que procesan 1M+ datos/día y sirven a 50k+ usuarios.

¿Te interesa algún proyecto en particular?"""

        elif any(word in msg_lower for word in ['disponible', 'available', 'contratar', 'hire']):
            return f"""📅 **Disponibilidad:**

{self.cv_data['availability']}

**🎯 Puedo ayudarte con:**
• Desarrollo de sistemas IA empresariales
• Integración de LLMs (GPT, Claude, DeepSeek)  
• Arquitectura de datos y MLOps
• Consultoría en transformación digital

**📧 Para proyectos, compárteme:**
• Tu email
• Descripción del proyecto
• Tecnologías involucradas

¡Te responderé en menos de 24h!"""

        elif any(word in msg_lower for word in ['contacto', 'contact']):
            return """📧 **Contacto profesional:**

Para proyectos o consultas, por favor comparte:
• 📧 **Tu email** (obligatorio)
• 🏢 **Tu empresa/proyecto**
• 💼 **Breve descripción** de lo que necesitas
• ⚡ **Tecnologías** involucradas

**Respuesta garantizada en 24 horas.**

*Especializado en IA, datos y soluciones enterprise.*"""

        else:
            return f"""🤖 Soy **{self.cv_data['name']}**, {self.cv_data['title']}.

**🧠 Especialista en:**
• Inteligencia Artificial y Machine Learning
• Sistemas enterprise y arquitectura de datos  
• LangGraph, CrewAI, OpenAI, LangChain

**💬 Puedes preguntarme sobre:**
• Mi experiencia técnica y proyectos
• Disponibilidad para nuevos proyectos
• Tecnologías específicas de IA
• Cómo podemos colaborar

**¿Qué te interesa saber específicamente?**"""

class TelegramBot:
    """🤖 Bot puro como Asuka"""
    
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
        """Handlers básicos"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando start"""
        cv = self.digital_twin.cv_data
        
        welcome = f"""🤖 **¡Hola! Soy el asistente de {cv['name']}**

*{cv['bio']}*

📍 {cv['location']}
💼 {cv['title']}
⚡ {cv['availability']}

**¡Pregúntame lo que quieras!**"""
        
        await update.message.reply_text(welcome, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando help"""
        help_text = """📋 **¿En qué puedo ayudarte?**

Pregúntame sobre:
• 💻 Experiencia y skills
• 🚀 Proyectos realizados
• 📅 Disponibilidad
• 📧 Contacto

**Ejemplos:**
• "¿Qué experiencia tienes?"
• "Cuéntame tus proyectos"
• "¿Estás disponible?"

*¡Solo escribe tu pregunta!*"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes"""
        try:
            # Mostrar typing
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action="typing"
            )
            
            # Procesar con Digital Twin
            response = await self.digital_twin.process_query(update.message.text)
            
            # Enviar respuesta
            await update.message.reply_text(response, parse_mode='Markdown')
            
            # Log
            user = update.effective_user
            print(f"👤 {user.first_name}: {update.message.text}")
            print(f"🤖 Respuesta enviada ({len(response)} chars)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await update.message.reply_text(
                "🤖 Disculpa, hubo un error. ¿Puedes repetir?"
            )
    
    async def cleanup_and_start(self):
        """Limpia conexiones y arranca"""
        try:
            print("🧹 Limpiando conexiones previas...")
            
            # Limpiar webhooks y updates pendientes
            await self.app.bot.delete_webhook(drop_pending_updates=True)
            await self.app.bot.get_updates(offset=-1, limit=1, timeout=1)
            print("✅ Conexiones limpiadas")
            
        except Exception as e:
            print(f"⚠️ Error en cleanup: {e}")
        
        print("🎯 Iniciando polling...")
    
    def start_bot(self):
        """Inicia el bot de forma síncrona"""
        # Usar el loop existente en lugar de crear uno nuevo
        try:
            # Obtener loop existente
            loop = asyncio.get_event_loop()
            
            # Hacer cleanup primero
            loop.run_until_complete(self.cleanup_and_start())
            
            # Iniciar polling sin crear nuevo loop
            self.app.run_polling(drop_pending_updates=True)
            
        except RuntimeError as e:
            if "event loop is already running" in str(e):
                print("⚠️ Event loop ya corriendo - modo alternativo")
                # Modo alternativo sin loop
                self.app.run_polling(drop_pending_updates=True)
            else:
                raise e

if __name__ == "__main__":
    print("🚀 INICIANDO BOT PURO...")
    
    bot = TelegramBot()
    
    # Ejecutar sin asyncio.run() para evitar conflicto de loops
    bot.start_bot()