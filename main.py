import asyncio
import feedparser
import os
from telegram import Bot

# --- CONFIGURACIÓN ---
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# Lista de fuentes MEJORADA
FUENTES = [
    {
        "nombre": "Google News (Boca)",
        # Este link es mágico: trae lo mejor de Olé, Infobae, etc. pero sin errores 404
        "url": "https://news.google.com/rss/search?q=Boca+Juniors&hl=es-419&gl=AR&ceid=AR:es-419"
    },
    {
        "nombre": "TyC Sports",
        "url": "https://www.tycsports.com/rss/boca-juniors.xml"
    },
    {
        "nombre": "ESPN",
        "url": "https://www.espn.com.ar/espn/rss/futbol/team?id=5"
    }
]

async def enviar_noticias():
    print("Buscando noticias...")
    try:
        bot = Bot(token=TOKEN)
        mensaje = "💙💛 **RESUMEN XENEIZE** 💛💙\n\n"
        hay_info = False

        for fuente in FUENTES:
            try:
                # feedparser a veces se confunde con Google, forzamos la lectura
                feed = feedparser.parse(fuente["url"])
                if feed.entries:
                    hay_info = True
                    mensaje += f"📢 *{fuente['nombre']}*\n"
                    # Sacamos las 2 primeras
                    for entry in feed.entries[:2]:
                        mensaje += f"🔹 {entry.title}\n🔗 {entry.link}\n\n"
                    mensaje += "----------------\n"
            except Exception as e:
                print(f"Saltando fuente {fuente['nombre']}: {e}")

        if hay_info:
            if len(mensaje) > 4000: mensaje = mensaje[:4000] + "..."
            await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')
            print("Enviado OK.")
        else:
            print("Nada nuevo por ahora.")

    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    asyncio.run(enviar_noticias())
