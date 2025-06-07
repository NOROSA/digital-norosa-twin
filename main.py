# 🤖 Tu Yo Virtual Profesional - CrewAI Nativo con YAML
# Usando archivos agents.yaml y tasks.yaml con DeepSeek

import os
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from contextlib import asynccontextmanager

# Telegram Bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# CrewAI Framework - NATIVO con YAML
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

# IMPORTANTE: Configurar variables de entorno para DeepSeek
os.environ["OPENAI_API_KEY"] = DEEPSEEK_API_KEY
os.environ["OPENAI_API_BASE"] = DEEPSEEK_BASE_URL

class DigitalTwin:
    """🤖 Tu representante virtual usando CrewAI con YAML"""
    
    def __init__(self):
        self.cv_data = self.load_cv_data()
        self.crew = None
        self.setup_crew()
    
    def load_cv_data(self) -> Dict[str, Any]:
        """Carga tu información profesional COMPLETA desde VARIABLES DE ENTORNO"""
        return {
            "name": os.getenv('CV_NAME', 'Norbert Rodríguez Sagarra'),
            "title": os.getenv('CV_TITLE', 'Senior AI Engineer & Intelligent Apps Project Manager'),
            "location": os.getenv('CV_LOCATION', 'Barcelona, España'),
            "bio": os.getenv('CV_BIO', 'Apasionado por la IA, datos y eficiencia...'),
            "personality": os.getenv('CV_PERSONALITY', 'Analítico, innovador, estratégico...'),
            
            # Skills completos
            "skills": os.getenv('CV_SKILLS', 'Python,LangGraph,CrewAI,OpenAI API,LangChain').split(','),
            
            # TODAS las experiencias (3 completas)
            "experience": [
                {
                    "company": os.getenv('CV_EXP1_COMPANY', 'VEOLIA-AGBAR-SYNECTIC (DEVOTEAM)'),
                    "role": os.getenv('CV_EXP1_ROLE', 'Senior AI Engineer & Project Manager'),
                    "years": os.getenv('CV_EXP1_YEARS', '2021-2024'),
                    "highlights": os.getenv('CV_EXP1_HIGHLIGHTS', 'Diseño e implementación de agentes IA avanzados...')
                },
                {
                    "company": os.getenv('CV_EXP2_COMPANY', 'IBM Collaborative Projects (Freelance)'),
                    "role": os.getenv('CV_EXP2_ROLE', 'AI Solutions Architect & Team Lead'),
                    "years": os.getenv('CV_EXP2_YEARS', '2017-2022'),
                    "highlights": os.getenv('CV_EXP2_HIGHLIGHTS', 'Liderazgo de proyectos IA con Watson...')
                },
                {
                    "company": os.getenv('CV_EXP3_COMPANY', 'Enterprise Consulting & Training'),
                    "role": os.getenv('CV_EXP3_ROLE', 'Tech Lead & Mobile Solutions Architect'),
                    "years": os.getenv('CV_EXP3_YEARS', '2017'),
                    "highlights": os.getenv('CV_EXP3_HIGHLIGHTS', 'Liderazgo de equipos desarrollo Android/iOS...')
                }
            ],
            
            # TODOS los proyectos (5 completos)
            "projects": [
                {
                    "name": os.getenv('CV_PROJ1_NAME', 'Enterprise AI Assistant Ecosystem'),
                    "tech": os.getenv('CV_PROJ1_TECH', 'LangGraph + CrewAI + Multiple LLMs + FastAPI + Snowflake'),
                    "description": os.getenv('CV_PROJ1_DESC', 'Sistema completo de asistentes IA para 50k+ empleados...')
                },
                {
                    "name": os.getenv('CV_PROJ2_NAME', 'AI-Powered Hydroelectric Prediction Platform'),
                    "tech": os.getenv('CV_PROJ2_TECH', 'Python + TensorFlow + BigQuery + Airflow + PowerBI + GCP'),
                    "description": os.getenv('CV_PROJ2_DESC', 'Plataforma ML para predicción energía hidroeléctrica...')
                },
                {
                    "name": os.getenv('CV_PROJ3_NAME', 'Intelligent Data Orchestration Suite'),
                    "tech": os.getenv('CV_PROJ3_TECH', 'Talend + DBT + Spark + SCADA + LangChain + Vector DBs'),
                    "description": os.getenv('CV_PROJ3_DESC', 'Orquestación inteligente datos multi-origen con IA...')
                },
                {
                    "name": os.getenv('CV_PROJ4_NAME', 'AI-Enhanced Enterprise Data Mining'),
                    "tech": os.getenv('CV_PROJ4_TECH', 'Python + Watson + Beautiful Soup + Apache Kafka + MLOps'),
                    "description": os.getenv('CV_PROJ4_DESC', 'Sistema scraping B2B con IA para análisis competencia...')
                },
                {
                    "name": os.getenv('CV_PROJ5_NAME', 'Cybersecurity AI Analyst'),
                    "tech": os.getenv('CV_PROJ5_TECH', 'Python + Metasploit + NMAP + LangChain + Vector Search'),
                    "description": os.getenv('CV_PROJ5_DESC', 'Asistente IA para análisis vulnerabilidades...')
                }
            ],
            
            # Información adicional completa
            "availability": os.getenv('CV_AVAILABILITY', 'Disponible para proyectos de IA, consultoría y transformación digital'),
            "education": os.getenv('CV_EDUCATION', 'BSc Data Science (UCM), Master Prompt Engineering...'),
            "ai_specialties": os.getenv('CV_AI_SPECIALTIES', 'LLM Orchestration,Agentic Workflows,RAG Systems...').split(','),
            "achievements": os.getenv('CV_ACHIEVEMENTS', 'Modernized legacy data ecosystems...'),
            "values": os.getenv('CV_VALUES', 'Driven by making the world better through useful technology...'),
            "languages": os.getenv('CV_LANGUAGES', 'Español (nativo), Catalán (nativo), Inglés (B2)'),
            "additional_projects": os.getenv('CV_ADDITIONAL_PROJECTS', 'CrewAI Multi-Agent Trading Bot...'),
            "additional_info": os.getenv('CV_ADDITIONAL_INFO', 'GitHub: n0r0s4, Kaggle: n0r0s4...')
        }
    
    def setup_crew(self):
        """Configura el crew usando archivos YAML nativos con DeepSeek"""
        try:
            # SOLUCIÓN CORREGIDA: Usar archivos YAML directamente
            # CrewAI buscará automáticamente agents.yaml y tasks.yaml en la carpeta actual
            # o en la carpeta config/
            
            # Verificar que los archivos YAML existan
            import os
            yaml_files = ['agents.yaml', 'tasks.yaml']
            config_files = ['config/agents.yaml', 'config/tasks.yaml']
            
            # Buscar archivos YAML
            yaml_found = all(os.path.exists(f) for f in yaml_files)
            config_found = all(os.path.exists(f) for f in config_files)
            
            if yaml_found:
                # Archivos en directorio raíz
                print("✅ Usando archivos YAML en directorio raíz")
                self.crew = Crew()
            elif config_found:
                # Archivos en carpeta config/
                print("✅ Usando archivos YAML en carpeta config/")
                self.crew = Crew(config_path="config")
            else:
                # No hay archivos YAML, crear crew programáticamente
                print("⚠️ No se encontraron archivos YAML, usando configuración por código")
                self.crew = self.create_fallback_crew()
            
            print("✅ CrewAI configurado correctamente")
            
        except Exception as e:
            print(f"Error setting up crew: {e}")
            print("🔄 Intentando configuración fallback...")
            self.crew = self.create_fallback_crew()
    
    def create_fallback_crew(self):
        """Crea crew programáticamente si no hay archivos YAML"""
        from crewai import Agent, Task
        
        try:
            # Crear agente principal
            cv_agent = Agent(
                role='Professional CV Expert & Representative',
                goal=f'Act as the professional representative of {self.cv_data["name"]}, showcasing experience and skills',
                backstory=f'''You are the virtual representative of {self.cv_data["name"]}, a skilled {self.cv_data["title"]}. 
                You know their complete career history, technical skills: {", ".join(self.cv_data["skills"])}, 
                and professional achievements.
                
                Personality: {self.cv_data["personality"]}
                
                You should:
                - Speak in first person as if you ARE {self.cv_data["name"]}
                - Be enthusiastic about technical projects
                - Highlight relevant experience for each question
                - Show personality while maintaining professionalism
                - Suggest next steps when someone shows interest''',
                verbose=True,
                allow_delegation=False
            )
            
            # Crear tarea principal
            response_task = Task(
                description='''Analyze the user query and provide a comprehensive professional response.
                
                User Query: {query}
                
                Professional Context Available:
                - Technical skills and experience
                - Project portfolio and achievements
                - Work history and current availability
                
                Provide a response that:
                - Directly answers their question
                - Highlights relevant experience
                - Shows enthusiasm and competence
                - Maintains authentic personality
                - Suggests logical next steps if appropriate''',
                agent=cv_agent,
                expected_output='A personalized, professional response that addresses the query and represents the professional authentically'
            )
            
            # Crear crew
            return Crew(
                agents=[cv_agent],
                tasks=[response_task],
                verbose=True
            )
            
        except Exception as e:
            print(f"Error creating fallback crew: {e}")
            return None
    
    async def process_query(self, user_message: str, context: str = "") -> str:
        """Procesa consulta del usuario usando CrewAI"""
        
        if self.crew:
            try:
                # Preparar contexto completo para los agentes
                professional_context = f"""
                INFORMACIÓN PROFESIONAL COMPLETA DE NORBERT:
                
                Nombre: {self.cv_data['name']}
                Título: {self.cv_data['title']}
                Ubicación: {self.cv_data['location']}
                Bio: {self.cv_data['bio']}
                Personalidad: {self.cv_data['personality']}
                Disponibilidad: {self.cv_data['availability']}
                
                SKILLS TÉCNICOS ({len(self.cv_data['skills'])} tecnologías):
                {', '.join(self.cv_data['skills'])}
                
                ESPECIALIDADES IA:
                {', '.join(self.cv_data.get('ai_specialties', []))}
                
                EXPERIENCIA LABORAL COMPLETA:
                """
                
                for i, exp in enumerate(self.cv_data['experience'], 1):
                    professional_context += f"""
                {i}. {exp['role']} en {exp['company']} ({exp['years']})
                   Logros: {exp['highlights']}
                """
                
                professional_context += f"""
                
                PROYECTOS DESTACADOS COMPLETOS ({len(self.cv_data['projects'])} proyectos):
                """
                
                for i, project in enumerate(self.cv_data['projects'], 1):
                    professional_context += f"""
                {i}. {project['name']} 
                   Tech Stack: {project['tech']}
                   Descripción: {project['description']}
                """
                
                professional_context += f"""
                
                EDUCACIÓN Y CERTIFICACIONES:
                {self.cv_data.get('education', 'Información educativa completa disponible')}
                
                LOGROS Y RECONOCIMIENTOS:
                {self.cv_data.get('achievements', 'Múltiples logros en transformación digital')}
                
                FILOSOFÍA Y VALORES:
                {self.cv_data.get('values', 'Orientado a soluciones tecnológicas útiles')}
                
                IDIOMAS:
                {self.cv_data.get('languages', 'Multilingüe')}
                
                PROYECTOS ADICIONALES:
                {self.cv_data.get('additional_projects', 'Múltiples proyectos paralelos')}
                
                INFORMACIÓN ADICIONAL:
                {self.cv_data.get('additional_info', 'Activo en comunidad tech')}
                
                CONSULTA DEL USUARIO:
                {user_message}
                
                CONTEXTO ADICIONAL:
                {context}
                """
                
                # Ejecutar crew con el contexto completo
                result = self.crew.kickoff(inputs={"query": professional_context})
                
                # Extraer el resultado final
                if hasattr(result, 'raw'):
                    return str(result.raw)
                else:
                    return str(result)
                
            except Exception as e:
                print(f"CrewAI execution error: {e}")
                return self.simple_response(user_message)
        else:
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
    """🤖 Bot de Telegram usando CrewAI con YAML"""
    
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
        """Maneja mensajes de texto usando CrewAI"""
        user_id = update.effective_user.id
        message = update.message.text
        
        # Si está en modo recolección de contacto
        if user_id in self.collecting_contacts:
            await self.process_contact_info(update, message)
            return
        
        # Mostrar que está escribiendo
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Procesar con Digital Twin (CrewAI)
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
            print(f"Error processing message: {e}")
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