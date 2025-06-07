# 🤖 Digital Twin - VERSIÓN MÍNIMA DE EMERGENCIA
# Esta versión arranca 100% seguro sin fallar

import os
import asyncio
from typing import Dict, Any
from contextlib import asynccontextmanager

print("🔍 INICIANDO IMPORTS...")

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
    print("✅ Telegram importado")
except Exception as e:
    print(f"❌ Error Telegram: {e}")
    exit(1)

try:
    from fastapi import FastAPI, Request
    print("✅ FastAPI importado")
except Exception as e:
    print(f"❌ Error FastAPI: {e}")
    exit(1)

print("✅ TODOS LOS IMPORTS BÁSICOS OK")

# Configuration - ULTRA DEFENSIVA
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
PORT = int(os.getenv('PORT', 8000))

print(f"🔑 TELEGRAM_TOKEN: {'✅ OK' if TELEGRAM_TOKEN else '❌ FALTA'}")
print(f"🔑 DEEPSEEK_API_KEY: {'✅ OK' if DEEPSEEK_API_KEY else '❌ FALTA'}")
print(f"🔑 WEBHOOK_URL: {WEBHOOK_URL or 'MODO POLLING'}")

class SimpleDigitalTwin:
    """🤖 Versión mínima que SIEMPRE funciona"""
    
    def __init__(self):
        print("🤖 Inicializando Digital Twin simple...")
        self.cv_data = self.load_basic_cv()
        self.use_ai = False
        
        # Solo intentar AI si hay API key
        if DEEPSEEK_API_KEY:
            try:
                self.setup_ai()
            except Exception as e:
                print(f"⚠️ AI falló, modo simple: {e}")
        
        print("✅ Digital Twin inicializado")
    
    def load_basic_cv(self) -> Dict[str, Any]:
        """Carga CV básico desde env vars"""
        return {
            "name": os.getenv('CV_NAME', 'Norbert Rodríguez Sagarra'),
            "title": os.getenv('CV_TITLE', 'Senior AI Engineer & Project Manager'),
            "location": os.getenv('CV_LOCATION', 'Barcelona, España'),
            "bio": os.getenv('CV_BIO', 'Experto en IA, datos y desarrollo de soluciones innovadoras'),
            "skills": os.getenv('CV_SKILLS', 'Python,AI,LangGraph,CrewAI,FastAPI,AWS').split(','),
            "availability": os.getenv('CV_AVAILABILITY', 'Disponible para proyectos de IA y consultoría'),
            "experience": [
                {
                    "company": "VEOLIA-AGBAR-SYNECTIC",
                    "role": "Senior AI Engineer",
                    "years": "2021-2024",
                    "highlights": "Sistemas IA empresariales para 50k+ usuarios"
                }
            ],
            "projects": [
                {
                    "name": "Enterprise AI Assistant Ecosystem",
                    "tech": "LangGraph + CrewAI + Multiple LLMs",
                    "description": "Sistema completo de asistentes IA empresariales"
                }
            ]
        }
    
    def setup_ai(self):
        """Intenta configurar AI de forma segura"""
        try:
            print("🧠 Intentando configurar IA...")
            
            # Configurar environment para OpenAI/DeepSeek
            os.environ["OPENAI_API_KEY"] = DEEPSEEK_API_KEY
            os.environ["OPENAI_API_BASE"] = DEEPSEEK_BASE_URL
            
            # Intentar import CrewAI
            from crewai import Crew, Agent, Task
            
            # Crear crew simple SIN EJECUTAR
            self.agent = Agent(
                role='AI Assistant',
                goal='Help users professionally',
                backstory=f'You are {self.cv_data["name"]}, an AI expert.',
                verbose=False,  # Cambiar a False para evitar logs
                allow_delegation=False
            )
            
            self.task_template = Task(
                description='Respond to user query professionally as Norbert: {query}',
                agent=self.agent,
                expected_output='Professional response'
            )
            
            # NO crear crew aún - solo guardar componentes
            self.use_ai = True
            print("✅ IA configurada correctamente")
            
        except Exception as e:
            print(f"⚠️ IA falló: {e}")
            self.use_ai = False
    
    async def process_query(self, message: str) -> str:
        """Procesa consulta - con o sin IA"""
        
        if self.use_ai:
            try:
                # Crear crew dinámicamente para cada consulta
                from crewai import Crew, Task
                
                # Crear tarea específica para esta consulta
                task = Task(
                    description=f'Respond to user query professionally as {self.cv_data["name"]}: {message}',
                    agent=self.agent,
                    expected_output='Professional response'
                )
                
                # Crear crew temporal
                crew = Crew(
                    agents=[self.agent],
                    tasks=[task],
                    verbose=False
                )
                
                # Ejecutar crew
                result = crew.kickoff()
                return str(result)
                
            except Exception as e:
                print(f"❌ Error IA: {e}")
                # Fallback a respuesta simple
        
        # Respuesta simple sin IA
        return self.simple_response(message)
    
    def simple_response(self, message: str) -> str:
        """Respuestas simples sin IA"""
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['hola', 'hello', 'hi']):
            return f"""👋 ¡Hola! Soy {self.cv_data['name']}, {self.cv_data['title']}.

{self.cv_data['bio']}

¿En qué puedo ayudarte?"""

        elif any(word in msg_lower for word in ['experiencia', 'skills', 'tecnolog']):
            return f"""🛠️ **Mi experiencia:**

**Skills:** {', '.join(self.cv_data['skills'])}

**Experiencia actual:** {self.cv_data['experience'][0]['role']} en {self.cv_data['experience'][0]['company']}

**Logros:** {self.cv_data['experience'][0]['highlights']}"""

        elif any(word in msg_lower for word in ['proyecto', 'portfolio']):
            return f"""🚀 **Proyectos destacados:**

**{self.cv_data['projects'][0]['name']}**
- Tech: {self.cv_data['projects'][0]['tech']}
- {self.cv_data['projects'][0]['description']}

¿Te interesa saber más?"""

        elif any(word in msg_lower for word in ['contacto', 'contact']):
            return """📧 **Contacto:**

Para proyectos o consultas, comparte:
• Tu email
• Descripción del proyecto

¡Te responderé pronto!"""

        else:
            return f"""🤖 Soy {self.cv_data['name']}, experto en IA y desarrollo.

Puedes preguntarme sobre:
• Mi experiencia técnica
• Proyectos realizados
• Disponibilidad
• Contacto

¿Qué te interesa saber?"""

class SimpleTelegramBot:
    """🤖 Bot ultra simple que SIEMPRE funciona"""
    
    def __init__(self):
        print("🤖 Inicializando bot...")
        self.digital_twin = SimpleDigitalTwin()
        
        if not TELEGRAM_TOKEN:
            print("❌ TELEGRAM_TOKEN requerido")
            exit(1)
            
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()
        print("✅ Bot inicializado")
    
    async def cleanup_previous_connections(self):
        """Limpia conexiones previas como hacía Asuka"""
        try:
            print("🧹 Limpiando conexiones previas...")
            
            # Eliminar webhook si existe
            await self.app.bot.delete_webhook(drop_pending_updates=True)
            print("✅ Webhook eliminado")
            
            # Limpiar updates pendientes
            await self.app.bot.get_updates(offset=-1, limit=1, timeout=1)
            print("✅ Updates pendientes limpiados")
            
        except Exception as e:
            print(f"⚠️ Error en cleanup: {e}")
            # No es crítico, continuar
    
    def setup_handlers(self):
        """Handlers básicos"""
        self.app.add_handler(CommandHandler("start", self.start_command))
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
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes"""
        try:
            # Mostrar typing
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Procesar respuesta
            response = await self.digital_twin.process_query(update.message.text)
            
            # Enviar respuesta
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            print(f"Error handling message: {e}")
            await update.message.reply_text("🤖 Disculpa, hubo un error. ¿Puedes repetir?")

# Lifespan para FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown - SIN webhooks como Asuka"""
    print("🚀 FastAPI iniciando...")
    
    # NO configurar webhooks - usar polling como Asuka
    print("🔄 Modo polling como Asuka (sin webhooks)")
    
    yield
    print("🔄 FastAPI cerrando...")

# Crear instancias
print("🏗️ Creando bot y app...")
bot = SimpleTelegramBot()
app = FastAPI(lifespan=lifespan)

@app.post(f"/webhook/{TELEGRAM_TOKEN}")
async def webhook(request: Request):
    """Webhook handler"""
    try:
        data = await request.json()
        update = Update.de_json(data, bot.app.bot)
        await bot.app.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/")
async def health():
    """Health check"""
    return {
        "status": "🤖 Digital Twin ACTIVO",
        "name": bot.digital_twin.cv_data['name'],
        "ai_enabled": bot.digital_twin.use_ai,
        "version": "emergency_stable"
    }

@app.get("/test")
async def test():
    """Test endpoint"""
    return {
        "telegram_ok": bool(TELEGRAM_TOKEN),
        "deepseek_ok": bool(DEEPSEEK_API_KEY),
        "webhook": WEBHOOK_URL or "polling",
        "cv_loaded": len(bot.digital_twin.cv_data) > 0
    }

if __name__ == "__main__":
    print("🚀 INICIANDO APLICACIÓN...")
    print("🔄 Modo Asuka (polling con cleanup)")
    
    async def run_bot_with_cleanup():
        """Ejecuta el bot con cleanup previo como Asuka"""
        await bot.cleanup_previous_connections()
        print("🎯 Iniciando polling...")
        bot.app.run_polling(
            drop_pending_updates=True,  # Como Asuka
            close_loop=False
        )
    
    # Ejecutar bot con cleanup
    import asyncio
    asyncio.run(run_bot_with_cleanup())