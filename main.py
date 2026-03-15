import asyncio
import feedparser
import os
import re
import logging
from datetime import datetime, timezone, timedelta
from telegram import Bot

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# --- CONFIGURACIÓN ---
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Zona horaria Argentina (UTC-3)
TZ_AR = timezone(timedelta(hours=-3))

# Keywords para filtrar noticias relevantes (al menos una debe aparecer en el título)
KEYWORDS = ["boca", "xeneize", "riquelme", "bombonera", "caverna"]

# Fuentes RSS — agregá o quitá las que quieras
FUENTES = [
    {
        "nombre": "Google News",
        "emoji": "🌐",
        "url": "https://news.google.com/rss/search?q=Boca+Juniors&hl=es-419&gl=AR&ceid=AR:es-419",
    },
    {
        "nombre": "TyC Sports",
        "emoji": "📺",
        "url": "https://www.tycsports.com/rss/boca-juniors.xml",
    },
    {
        "nombre": "ESPN",
        "emoji": "🏟️",
        "url": "https://www.espn.com.ar/espn/rss/futbol/team?id=5",
    },
    {
        "nombre": "Olé",
        "emoji": "📰",
        "url": "https://www.ole.com.ar/rss/boca-juniors/",
    },
    {
        "nombre": "Infobae Deportes",
        "emoji": "📡",
        "url": "https://www.infobae.com/feeds/rss/deportes/",
    },
]

# Cantidad de noticias por fuente
NOTICIAS_POR_FUENTE = 3


def _normalizar(titulo: str) -> str:
    """Normaliza un título para detectar duplicados."""
    texto = titulo.lower().strip()
    texto = re.sub(r"[^\w\s]", "", texto)  # quitar puntuación
    texto = re.sub(r"\s+", " ", texto)  # colapsar espacios
    return texto


def _es_relevante(titulo: str) -> bool:
    """Devuelve True si el título menciona al menos un keyword."""
    titulo_lower = titulo.lower()
    return any(kw in titulo_lower for kw in KEYWORDS)


def _escapar_markdown_v2(texto: str) -> str:
    """Escapa caracteres especiales para MarkdownV2 de Telegram."""
    caracteres = r"_[]()~`>#+-=|{}.!"
    for c in caracteres:
        texto = texto.replace(c, f"\\{c}")
    return texto


async def enviar_noticias():
    log.info("🔍 Buscando noticias de Boca Juniors...")

    bot = Bot(token=TOKEN)
    fecha = datetime.now(TZ_AR).strftime("%d/%m/%Y")
    titulos_vistos: set[str] = set()
    bloques: list[str] = []

    for fuente in FUENTES:
        try:
            feed = feedparser.parse(fuente["url"])
            if not feed.entries:
                log.warning("Sin entradas para %s", fuente["nombre"])
                continue

            lineas: list[str] = []
            for entry in feed.entries:
                # Filtro de relevancia
                if not _es_relevante(entry.title):
                    continue

                # Deduplicación
                clave = _normalizar(entry.title)
                if clave in titulos_vistos:
                    continue
                titulos_vistos.add(clave)

                titulo_esc = _escapar_markdown_v2(entry.title)
                link = entry.link
                lineas.append(f"  🔹 [{titulo_esc}]({link})")

                if len(lineas) >= NOTICIAS_POR_FUENTE:
                    break

            if lineas:
                nombre_esc = _escapar_markdown_v2(fuente["nombre"])
                encabezado = f"{fuente['emoji']} *{nombre_esc}*"
                bloques.append(encabezado + "\n" + "\n".join(lineas))

        except Exception as e:
            log.error("Error con fuente %s: %s", fuente["nombre"], e)

    if not bloques:
        log.info("No se encontraron noticias relevantes.")
        return

    fecha_esc = _escapar_markdown_v2(fecha)
    header = f"💙💛 *RESUMEN XENEIZE* 💛💙\n📅 {fecha_esc}\n"
    separador = "\n━━━━━━━━━━━━━━━━━━━━\n"
    mensaje = header + separador + separador.join(bloques) + separador

    # Telegram limita a 4096 caracteres
    if len(mensaje) > 4000:
        mensaje = mensaje[:3997] + "\\.\\.\\."

    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=mensaje,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
        )
        log.info("✅ Mensaje enviado correctamente.")
    except Exception as e:
        log.error("Error al enviar mensaje: %s", e)


if __name__ == "__main__":
    asyncio.run(enviar_noticias())
