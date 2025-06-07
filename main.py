# 🤖 Tu Yo Virtual Profesional - CrewAI Nativo
# Simple, limpio y usando el YAML nativo de CrewAI

import os
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

# Telegram Bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# CrewAI Framework - NATIVO
from crewai import Crew

# FastAPI for Railway deployment
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
PORT = int(os.getenv('PORT', 8000))

# Email notification settings
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')

class DigitalTwin:
    """🤖 Tu representante virtual usando CrewAI nativo"""
    
    def __init__(self):
        self.cv_data = self.load_cv_data()
        self.crew = None
        self.setup_crew()
    
    def load_cv_data(self) -> Dict[str, Any]:
        """Carga tu información profesional desde VARIABLES DE ENTORNO (seguro)"""
        return {
            "name": os.getenv('CV_NAME', 'Tu Nombre'),
            "title": os.getenv('CV_TITLE', 'Senior Full Stack Developer'),
            "location": os.getenv('CV_LOCATION', 'Barcelona, España'),
            "bio": os.getenv('CV_BIO', 'Desarrollador con +5 años creando soluciones web innovadoras'),
            "personality": os.getenv('CV_PERSONALITY', 'Directo, entusiasta, con sentido del humor'),
            
            # Skills como string separado por comas
            "skills": os.getenv('CV_SKILLS', 'Python,JavaScript,React,FastAPI,AWS').split(','),
            
            # Experiencia (formato simple)
            "experience": [
                {
                    "company": os.getenv('CV_EXP1_COMPANY', 'Tech Startup'),
                    "role": os.getenv('CV_EXP1_ROLE', 'Senior Developer'),
                    "years": os.getenv('CV_EXP1_YEARS', '2022-2024'),
                    "highlights": os.getenv('CV_EXP1_HIGHLIGHTS', 'Lideré equipo, reduje latencia 40%, implementé CI/CD')
                },
                {
                    "company": os.getenv('CV_EXP2_COMPANY', 'Consultora Digital'),
                    "role": os.getenv('CV_EXP2_ROLE', 'Full Stack Developer'),
                    "years": os.getenv('CV_EXP2_YEARS', '2020-2022'),
                    "highlights": os.getenv('CV_EXP2_HIGHLIGHTS', 'Desarrollé 8+ proyectos cliente, stack MERN especialista')
                }
            ],
            
            # Proyectos
            "projects": [
                {
                    "name": os.getenv('CV_PROJ1_NAME', 'E-commerce Platform'),
                    "tech": os.getenv('CV_PROJ1_TECH', 'React + FastAPI + PostgreSQL'),
                    "description": os.getenv('CV_PROJ1_DESC', 'Plataforma con +10k usuarios activos')
                },
                {
                    "name": os.getenv('CV_PROJ2_NAME', 'AI Chat Assistant'),
                    "tech": os.getenv('CV_PROJ2_TECH', 'Python + OpenAI + Telegram'),
                    "description": os.getenv('CV_PROJ2_DESC', 'Bot inteligente con 95% satisfacción usuario')
                }
            ],
            
            "availability": os.getenv('CV_AVAILABILITY', 'Disponible para proyectos freelance')
        }
    
    def setup_crew(self):
        """Configura el crew usando archivos YAML nativos"""
        # CrewAI buscará automáticamente agents.yaml y tasks.yaml
        try:
            self.crew = Crew()
        except Exception as e:
            print(f"Error setting up crew: {e}")
            # Fallback simple si no hay archivos YAML
            self.crew = None
    
    async def process_query(self, user_message: str, context: str = "") -> str:
        """Procesa consulta del usuario"""
        
        if self.crew:
            # Usar CrewAI si está configurado
            try:
                # Contextualizar con datos del CV
                full_context = f"""
                INFORMACIÓN DEL PROFESIONAL:
                Nombre: {self.cv_data['name']}
                Título: {self.cv_data['title']}
                Bio: {self.cv_data['bio']}
                Skills: {', '.join(self.cv_data['skills'])}
                Disponibilidad: {self.cv_data['availability']}
                
                CONSULTA DEL USUARIO: {user_message}
                CONTEXTO ADICIONAL: {context}
                
                Responde como si fueras {self.cv_data['name']}, de manera profesional pero cercana.
                Si detectas interés en contratación, sugiere dejar datos de contacto.
                """
                
                result = self.crew.kickoff(inputs={"query": full_context})
                return str(result)
                
            except Exception as e:
                print(f"CrewAI error: {e}")
                # Fallback a respuesta simple
                return self.simple_response(user_message)
        else:
            # Respuesta simple sin CrewAI
            return self.simple_response(user_message)
    
    def simple_response(self, user_message: str) -> str:
        """Respuesta simple basada en keywords (fallback)"""
        message_lower = user_message.lower()
        
        # Detectar tipo de consulta
        if any(word in message_lower for word in ['experiencia', 'experience', 'skills', 'tecnolog']):
            return f"""
🛠️ **Mi experiencia técnica:**

**Skills principales:** {', '.join(self.cv_data['skills'])}

**Experiencia reciente:**
{self.cv_data['experience'][0]['role']} en {self.cv_data['experience'][0]['company']} ({self.cv_data['experience'][0]['years']})
• {self.cv_data['experience'][0]['highlights']}

¿Hay alguna tecnología específica que te interese conocer más?
            """
        
        elif any(word in message_lower for word in ['proyecto', 'project', 'portfolio']):
            projects_text = "🚀 **Mis proyectos destacados:**\n\n"
            for project in self.cv_data['projects']:
                projects_text += f"**{project['name']}**\n"
                projects_text += f"Tech: {project['tech']}\n"
                projects_text += f"{project['description']}\n\n"
            
            projects_text += "¿Te interesa alguno en particular?"
            return projects_text
        
        elif any(word in message_lower for word in ['disponible', 'available', 'contratar', 'hire']):
            return f"""
📅 **Disponibilidad actual:**

{self.cv_data['availability']}

¡Me interesa saber más sobre tu proyecto! 

¿Podrías contarme:
• ¿Qué tipo de proyecto es?
• ¿Qué tecnologías necesitas?
• ¿Cuál es tu email para mandarte más info?
            """
        
        elif any(word in message_lower for word in ['contacto', 'contact', 'email', 'teléfono']):
            return """
📧 **¡Perfecto! Quieres contactar conmigo**

Para conectarte directamente, por favor compárteme:
• 📧 Tu email (obligatorio)
• 📱 Tu teléfono (opcional) 
• 💼 Breve descripción del proyecto

Te responderé en menos de 24 horas.
            """
        
        else:
            return f"""
👋 ¡Hola! Soy {self.cv_data['name']}, {self.cv_data['title']}.

{self.cv_data['bio']}

**Puedes preguntarme sobre:**
• Mi experiencia técnica
• Proyectos que he realizado  
• Disponibilidad para nuevos proyectos
• Cómo contactarme

¿En qué puedo ayudarte específicamente?
            """

class TelegramBot:
    """🤖 Bot de Telegram sencillo pero efectivo"""
    
    def __init__(self):
        self.digital_twin = DigitalTwin()
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()
        
        # Para tracking de contactos
        self.collecting_contacts = set()
    
    def setup_handlers(self):
        """Configura handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("portfolio", self.portfolio_command))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🚀 Comando inicial"""
        cv = self.digital_twin.cv_data
        
        welcome = f"""
🤖 **¡Hola! Soy el asistente virtual de {cv['name']}**

*{cv['bio']}*

📍 {cv['location']}
💼 {cv['title']}
⚡ {cv['availability']}

**¿Qué te interesa saber?**
        """
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("💼 Ver Portfolio", callback_data="portfolio"),
                InlineKeyboardButton("🚀 Proyectos", callback_data="projects")
            ],
            [
                InlineKeyboardButton("📧 Contactar", callback_data="contact"),
                InlineKeyboardButton("❓ Preguntar", callback_data="ask")
            ]
        ])
        
        await update.message.reply_text(welcome, parse_mode='Markdown', reply_markup=keyboard)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📋 Ayuda"""
        help_text = f"""
📋 **¿En qué puedo ayudarte?**

**Pregúntame sobre:**
• 💻 Experiencia y skills técnicos
• 🚀 Proyectos realizados
• 📅 Disponibilidad para proyectos
• 📧 Cómo contactar con {self.digital_twin.cv_data['name']}

**Ejemplos de preguntas:**
• "¿Tienes experiencia en React?"
• "¿Qué proyectos has hecho?"
• "¿Estás disponible para un proyecto?"

*¡Solo escribe tu pregunta!*
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def portfolio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """💼 Portfolio completo"""
        cv = self.digital_twin.cv_data
        
        portfolio = f"""
💼 **Portfolio de {cv['name']}**

**🛠️ Skills:**
{', '.join(cv['skills'])}

**💼 Experiencia:**
"""
        
        for exp in cv['experience']:
            portfolio += f"""
**{exp['role']}** @ {exp['company']} ({exp['years']})
{exp['highlights']}

"""
        
        portfolio += "**🚀 Proyectos:**\n"
        for project in cv['projects']:
            portfolio += f"""
**{project['name']}**
Tech: {project['tech']}
{project['description']}

"""
        
        portfolio += f"**📋 Estado:** {cv['availability']}"
        
        await update.message.reply_text(portfolio, parse_mode='Markdown')
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja botones"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "portfolio":
            await self.portfolio_command(update, context)
        elif query.data == "projects":
            await self.show_projects(query)
        elif query.data == "contact":
            await self.start_contact_collection(query)
        elif query.data == "ask":
            await query.edit_message_text(
                "❓ **¡Perfecto!** Escribe tu pregunta.\n\n"
                "*Ejemplo: '¿Tienes experiencia con APIs?'*",
                parse_mode='Markdown'
            )
    
    async def show_projects(self, query):
        """Muestra proyectos"""
        projects = self.digital_twin.cv_data['projects']
        
        text = "🚀 **Proyectos Destacados:**\n\n"
        for i, project in enumerate(projects, 1):
            text += f"""
**{i}. {project['name']}**
🛠️ {project['tech']}
📋 {project['description']}

"""
        text += "*¿Alguno te llama la atención?*"
        
        await query.edit_message_text(text, parse_mode='Markdown')
    
    async def start_contact_collection(self, query):
        """Inicia recolección de contacto"""
        user_id = query.from_user.id
        self.collecting_contacts.add(user_id)
        
        text = f"""
📧 **Contactar con {self.digital_twin.cv_data['name']}**

*¡Perfecto! Le haré llegar tu información.*

**Comparte por favor:**
• 📧 Tu email
• 📱 Tu teléfono (opcional)
• 💼 Qué proyecto tienes en mente

**Ejemplo:**
"Mi email es juan@empresa.com
Necesito una web con React"

*Te responderá en menos de 24 horas.*
        """
        
        await query.edit_message_text(text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de texto"""
        user_id = update.effective_user.id
        message = update.message.text
        
        # Si está en modo recolección de contacto
        if user_id in self.collecting_contacts:
            await self.process_contact_info(update, message)
            return
        
        # Mostrar que está escribiendo
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Procesar con Digital Twin
            response = await self.digital_twin.process_query(message)
            
            # Enviar respuesta
            await update.message.reply_text(response, parse_mode='Markdown')
            
            # Detectar si muestra interés en contratación
            if any(word in message.lower() for word in ['proyecto', 'contratar', 'hire', 'trabajo', 'presupuesto']):
                await asyncio.sleep(1)
                await update.message.reply_text(
                    "💡 *¿Te interesa? Puedo conectarte directamente con él usando /contact*",
                    parse_mode='Markdown'
                )
        
        except Exception as e:
            await update.message.reply_text(
                "🤖 *Disculpa, hubo un pequeño error. ¿Puedes repetir?*",
                parse_mode='Markdown'
            )
    
    async def process_contact_info(self, update: Update, message: str):
        """Procesa información de contacto"""
        user_id = update.effective_user.id
        user_info = update.effective_user
        
        # Extraer email (básico)
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        
        if emails:
            # Guardar lead
            lead_info = {
                "email": emails[0],
                "message": message,
                "telegram_user": user_info.username or user_info.first_name,
                "user_id": user_id
            }
            
            # Enviar notificación
            await self.send_notification(lead_info)
            
            # Confirmar al usuario
            await update.message.reply_text(
                f"""
✅ **¡Perfecto! Información recibida**

📧 Email: {emails[0]}
💬 Mensaje: ✓

{self.digital_twin.cv_data['name']} recibirá tu información y te contactará pronto.

*¡Gracias por tu interés!*
                """,
                parse_mode='Markdown'
            )
            
            # Quitar de modo recolección
            self.collecting_contacts.discard(user_id)
            
        else:
            await update.message.reply_text(
                "📧 *No veo un email válido. ¿Puedes incluirlo?*\n\n"
                "*Ejemplo: juan@empresa.com*",
                parse_mode='Markdown'
            )
    
    async def send_notification(self, lead_info: Dict[str, Any]):
        """Envía notificación por email"""
        if not all([EMAIL_USER, EMAIL_PASS, NOTIFICATION_EMAIL]):
            print("Email not configured, skipping notification")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = NOTIFICATION_EMAIL
            msg['Subject'] = f"🔔 Nuevo Lead - {lead_info['telegram_user']}"
            
            body = f"""
🤖 Tu Digital Twin ha captado un nuevo lead!

📧 Email: {lead_info['email']}
👤 Usuario: {lead_info['telegram_user']}
💬 Mensaje:
{lead_info['message']}

¡Respóndele pronto!
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            text = msg.as_string()
            server.sendmail(EMAIL_USER, NOTIFICATION_EMAIL, text)
            server.quit()
            
            print(f"Notification sent for lead: {lead_info['email']}")
            
        except Exception as e:
            print(f"Failed to send notification: {e}")

# FastAPI app para Railway
app = FastAPI()
bot = TelegramBot()

@app.post(f"/webhook/{TELEGRAM_TOKEN}")
async def webhook(request: Request):
    """Webhook para Telegram"""
    try:
        data = await request.json()
        update = Update.de_json(data, bot.app.bot)
        await bot.app.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error"}

@app.get("/")
async def health():
    """Health check"""
    return {
        "status": "🤖 Digital Twin activo",
        "name": bot.digital_twin.cv_data['name'],
        "available": True
    }

@app.on_event("startup")
async def startup():
    """Configurar webhook"""
    if WEBHOOK_URL:
        webhook_url = f"{WEBHOOK_URL}/webhook/{TELEGRAM_TOKEN}"
        await bot.app.bot.set_webhook(webhook_url)
        print(f"🤖 Webhook configurado: {webhook_url}")

if __name__ == "__main__":
    import uvicorn
    
    if WEBHOOK_URL:
        # Modo producción con webhooks (Railway)
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    else:
        # Modo desarrollo simple con polling (como Asuka)
        print("🤖 Iniciando en modo desarrollo (polling)...")
        bot.app.run_polling()