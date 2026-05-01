# 🎯 Taskchamp Capture Bot

<p align="center">
  <b>Capture tasks from Telegram → Taskwarrior → Sync Server</b>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#deploy">Deploy</a>
</p>

---

## ✨ Features

- ⚡ **Instant Capture** — Send a message, get a task. No commands, no friction.
- 🔄 **Auto-Sync** — Tasks sync immediately to your Taskchampion server.
- 👥 **Multi-Account** — Use multiple Telegram accounts with one bot.
- 🛡️ **Secure** — Only authorized users can access, silent rejects for others.
- 🐳 **Dockerized** — One command deployment.
- 💡 **Smart Errors** — Helpful suggestions when you make mistakes.

---

## 🚀 Quick Start

```bash
# 1. Clone and enter directory
git clone <your-repo-url>
cd taskchamp-capture-bot

# 2. Configure environment
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN and ALLOWED_USER_IDS

# 3. Create taskrc with your sync server settings
cat > taskrc << 'EOF'
confirmation=off
data.location=/root/.task
sync.server.url=https://your-sync-server.com
sync.server.client_id=your-client-id
sync.encryption_secret=your-secret
EOF

# 4. Deploy
docker-compose up -d

# 5. Test
# Send a message to your bot on Telegram!
```

📖 **Full deployment guide**: [DEPLOY.md](DEPLOY.md)

---

## 💬 Usage

Just send any message to your bot:

```
You: Buy milk due:tomorrow +groceries project:home

Bot:
✅ Added

Synced ✓
```

### Taskwarrior Syntax

Full Taskwarrior syntax is supported:

| Feature | Example |
|---------|---------|
| Due dates | `due:tomorrow`, `due:friday`, `due:2025-05-01` |
| Tags | `+urgent`, `+shopping` |
| Projects | `project:work`, `project:personal` |
| Priority | `priority:H`, `priority:M` |
| Scheduled | `scheduled:monday` |

**Examples:**
- `Call dentist due:friday +calls`
- `Finish report project:work priority:H due:eod`
- `Buy groceries +shopping +home due:saturday`

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | From [@BotFather](https://t.me/BotFather) |
| `ALLOWED_USER_IDS` | ✅ Yes | Comma-separated Telegram user IDs |
| `TASKRC_PATH` | No | Taskrc path (default: `/root/.taskrc`) |
| `TASK_DATA_DIR` | No | Data directory (default: `/root/.task`) |
| `LOG_LEVEL` | No | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### Multi-Account Setup

Allow multiple Telegram accounts (all share the same task database):

```env
ALLOWED_USER_IDS=123456789,987654321,555666777
```

Get your user ID from [@userinfobot](https://t.me/userinfobot).

---

## 📦 Deploy

### Requirements

- Docker & Docker Compose
- Taskchampion sync server (running)

### Commands

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Update
docker-compose up -d --build
```

See [DEPLOY.md](DEPLOY.md) for troubleshooting and detailed setup.

---

## 🛠️ Tech Stack

- **Python 3.11** + asyncio
- **python-telegram-bot** v21
- **Taskwarrior** CLI
- **Docker** + Compose

---

## 🗺️ Roadmap

- [x] Core task capture
- [x] Auto-sync
- [x] Multi-user support
- [x] Docker deployment
- [ ] Voice message support (speech-to-text)
- [ ] Task listing / search
- [ ] Task modification

---

## 📄 License

MIT © 2024

---

<p align="center">
  Made with ❤️ for productivity nerds
</p>
