import asyncio
import feedparser
import os
from telegram import Bot

# --- CONFIGURACIÓN DE LA NUBE ---
# Ahora las llaves las saca de los "Secretos" de GitHub
TOKEN = os.environ['8540812072:AAFTlBXZo2FmbjFo2RCKFnyUQZoVY18AcK8']
CHAT_ID = os.environ['496903409']

FUENTES = [
    {"nombre": "Diario Olé", "url": "https://www.ole.com.ar/rss/boca-juniors/"},
    {"nombre": "TyC Sports", "url": "https://www.tycsports.com/rss/boca-juniors.xml"},
    {"nombre": "ESPN", "url": "https://www.espn.com.ar/espn/rss/futbol/team?id=5"}
]

async def enviar_noticias():
    print("Iniciando bot en la nube...")
    try:
        bot = Bot(token=TOKEN)
        mensaje = "💙💛 **Noticias desde la Nube** 💛💙\n\n"
        hay_info = False

        for fuente in FUENTES:
            try:
                feed = feedparser.parse(fuente["url"])
                if feed.entries:
                    hay_info = True
                    mensaje += f"📢 *{fuente['nombre']}*\n"
                    # Sacamos las 2 noticias más nuevas
                    for entry in feed.entries[:2]:
                        mensaje += f"🔹 {entry.title}\n🔗 {entry.link}\n\n"
                    mensaje += "----------------\n"
            except Exception as e:
                print(f"Error leyendo {fuente['nombre']}: {e}")

        if hay_info:
            if len(mensaje) > 4000: mensaje = mensaje[:4000] + "..."
            await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')
            print("¡Noticias enviadas con éxito!")
        else:
            print("No encontré noticias nuevas.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    asyncio.run(enviar_noticias())