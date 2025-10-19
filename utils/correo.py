import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def enviar_correo_agendamiento(destinatario, codigo):
    """
    Envía un correo de confirmación de agendamiento al paciente.
    """
    try:
        # Configurar mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] = EMAIL_SENDER
        mensaje["To"] = destinatario
        mensaje["Subject"] = "Confirmación de inicio de sesión - BeautyAngels"

        cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f7; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; 
                    border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
                    padding: 30px; text-align: center;">
            <h2 style="color: #c69838;">¡Hola!</h2>
            <p style="font-size: 16px; color: #555;">
                Tu <strong>código de verificación</strong> es:
            </p>
            <div style="font-size: 36px; font-weight: bold; color: #c69838; margin: 20px 0;">
                {codigo}
            </div>
            <p style="font-size: 14px; color: #999;">
                Este código expirará en 10 minutos. No lo compartas con nadie.
            </p>
            <hr style="margin: 30px 0;">
            <p style="font-size: 12px; color: #aaa;">
                © 2025 BeautyAngels — Todos los derechos reservados
            </p>
        </div>
    </body>
    </html>
    """
        mensaje.attach(MIMEText(cuerpo, "html"))

        # Enviar correo (usando Gmail)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(mensaje)

        print(f"✅ Correo enviado exitosamente a {destinatario}")
        return True

    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
        return False