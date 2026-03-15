# 💙💛 Bot Boca Juniors

Bot de Telegram que envía un resumen diario de noticias de Boca Juniors agregando múltiples fuentes RSS.

## ⚡ Setup rápido

1. **Forkeá** este repositorio
2. Creá un bot de Telegram con [@BotFather](https://t.me/BotFather) y copiá el token
3. Obtené tu `CHAT_ID` (podés usar [@userinfobot](https://t.me/userinfobot))
4. En tu fork → **Settings → Secrets and variables → Actions** → agregá:
   - `TELEGRAM_TOKEN` → el token de tu bot
   - `CHAT_ID` → tu chat ID
5. Habilitá GitHub Actions en la pestaña **Actions**

El bot enviará noticias automáticamente a las **09:00** y **21:00** hora Argentina. También podés ejecutarlo manualmente desde la pestaña Actions → **Run workflow**.

## 📰 Fuentes RSS

| Fuente | Emoji |
|--------|-------|
| Google News | 🌐 |
| TyC Sports | 📺 |
| ESPN | 🏟️ |
| Olé | 📰 |
| Infobae Deportes | 📡 |

Para agregar o quitar fuentes, editá la lista `FUENTES` en `main.py`.

## ⏰ Cambiar horarios

Editá los cron en `.github/workflows/noticias.yml`:

```yaml
schedule:
  - cron: '0 12 * * *'  # 09:00 AM Argentina
  - cron: '0 0 * * *'   # 21:00 PM Argentina
```

> Los horarios están en UTC. Argentina = UTC - 3.

## 🔧 Ejecución local

```bash
export TELEGRAM_TOKEN="tu-token"
export CHAT_ID="tu-chat-id"
pip install -r requirements.txt
python main.py
```

## 📂 Estructura

```
bot-boca/
├── main.py                          # Script principal
├── requirements.txt                 # Dependencias (fijadas)
├── README.md
└── .github/workflows/noticias.yml   # Cron de GitHub Actions
```
