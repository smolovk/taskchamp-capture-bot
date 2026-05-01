# Deploy Instructions

Deploy Taskchamp Capture Bot in 2 minutes.

## Quick Deploy (Production)

### 1. Create Directory & Files

```bash
mkdir taskchamp-bot && cd taskchamp-bot
```

### 2. Paste docker-compose.yml

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    image: docker.s1ngle.xyz/taskchamp-bot:latest
    container_name: taskchamp-bot
    env_file: .env
    volumes:
      - task_data:/root/.task
      - ./taskrc:/root/.taskrc:ro
    restart: unless-stopped

volumes:
  task_data:
```

### 3. Configure Environment

Create `.env`:

```bash
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=your_bot_token_here
ALLOWED_USER_IDS=your_telegram_user_id
EOF
```

Edit with your actual values:
- **Token**: Get from [@BotFather](https://t.me/BotFather) → `/newbot`
- **User ID**: Get from [@userinfobot](https://t.me/userinfobot)

Multiple accounts: `ALLOWED_USER_IDS=id1,id2,id3`

### 4. Configure Taskwarrior

Create `taskrc`:

```bash
cat > taskrc << 'EOF'
confirmation=off
data.location=/root/.task
sync.server.url=https://your-sync-server.com
sync.server.client_id=your-client-id
sync.encryption_secret=your-secret
EOF
```

### 5. Run

```bash
docker-compose up -d
```

Done! Send a message to your bot on Telegram.

---

## Management

```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Update to latest image
docker-compose pull && docker-compose up -d
```

---

## Development / Building

If you need to build the image locally (see Dockerfile for build commands):

```bash
# Clone repo
git clone <repo-url> && cd taskchamp-capture-bot

# Build (command is in Dockerfile comments)
docker build -t docker.s1ngle.xyz/taskchamp-bot:latest .

# Push
docker push docker.s1ngle.xyz/taskchamp-bot:latest
```

---

## Troubleshooting

### Bot doesn't respond

```bash
# Check logs
docker-compose logs -f

# Verify env
cat .env

# Check if taskrc exists
ls -la taskrc
```

### Tasks not syncing

```bash
# Test sync manually
docker-compose exec bot task sync
```

### Permission denied

```bash
chmod 644 taskrc
```

---

## Files Summary

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Service definition (uses pre-built image) |
| `.env` | Telegram token & authorized user IDs |
| `taskrc` | Taskwarrior & sync server configuration |
