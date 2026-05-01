# Deploy Instructions

Complete step-by-step guide to deploy Taskchamp Capture Bot.

## Prerequisites

- Docker and Docker Compose installed
- Your Taskchampion sync server running and accessible
- Telegram account

## Step 1: Get Credentials

### 1.1 Get Bot Token from @BotFather

1. Open Telegram and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Give your bot a name (e.g., "My Task Bot")
4. Give it a username ending in "bot" (e.g., "mytaskcapturebot")
5. **Copy the bot token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 1.2 Get Your User ID from @userinfobot

1. Open Telegram and search for **@userinfobot**
2. Start a chat
3. **Copy your numeric ID** (looks like: `123456789`)

## Step 2: Configure Environment

On your server:

```bash
# Clone or navigate to the project directory
cd taskchamp-capture-bot

# Copy the environment template
cp .env.example .env

# Edit the .env file
nano .env
```

Fill in the two required values:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ALLOWED_USER_IDS=123456789
```

**For multiple Telegram accounts**, use comma-separated IDs:
```env
ALLOWED_USER_IDS=123456789,987654321,555666777
```

Save and exit (Ctrl+O, Enter, Ctrl+X in nano).

## Step 3: Prepare Taskwarrior Config

Create your `taskrc` file with sync server settings:

```bash
cat > taskrc << 'EOF'
# Disable confirmation prompts
confirmation=off

# Task data location (inside container)
data.location=/root/.task

# =============================================================================
# TASKCHAMPION SYNC SERVER CONFIGURATION
# Replace with your actual sync server details
# =============================================================================

# Sync server URL (required)
sync.server.url=https://your-sync-server.example.com

# Client ID for this device (required)
# Generate with: uuidgen or task sync init
sync.server.client_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Encryption secret (required)
# Must match what you used during sync initialization
sync.encryption_secret=your-encryption-secret-here
EOF
```

**Important:** Replace the placeholders with your actual sync server configuration.

## Step 4: Deploy

### First Time Deploy

```bash
# Build the image and start the container
docker-compose up -d --build

# Check if it's running
docker-compose ps

# View logs to verify it's working
docker-compose logs -f
```

You should see output like:
```
2024-01-15 10:30:00 - Taskchamp Capture Bot - INFO - Starting Taskchamp Capture Bot...
2024-01-15 10:30:00 - Taskchamp Capture Bot - INFO - Authorized users: [123456789]
```

Press `Ctrl+C` to exit log view (container keeps running).

### Test the Bot

1. Open Telegram
2. Find your bot (by the username you created)
3. Send: `Test task due:today`
4. You should receive:
   ```
   ✅ Added

   Synced ✓
   ```

## Step 5: Managing the Bot

### View Logs

```bash
# View logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# View logs with timestamps
docker-compose logs -f -t
```

### Restart

```bash
docker-compose restart
```

### Update to New Version

```bash
# Pull latest changes (if using git)
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Stop

```bash
# Stop the bot
docker-compose down

# Stop and remove all data (WARNING: deletes tasks!)
docker-compose down -v
```

## Troubleshooting

### Bot doesn't respond

1. Check logs: `docker-compose logs -f`
2. Verify token is correct in `.env`
3. Ensure user ID(s) are correct (no quotes, just numbers, comma-separated for multiple)

### Tasks not syncing

1. Check taskrc has correct sync server config
2. Verify sync server is accessible from the container:
   ```bash
   docker-compose exec bot task sync
   ```
3. Check sync credentials (client_id, encryption_secret)

### Permission denied errors

Ensure taskrc is readable:
```bash
chmod 644 taskrc
```

### Container won't start

Check environment variables:
```bash
docker-compose config  # Validates config
docker-compose logs    # Shows error details
```

## Security Notes

- Keep `.env` file secure - it contains your bot token
- The `taskrc` file contains your sync encryption secret
- Never commit these files to git (they are gitignored)
- Only the configured user ID(s) can use the bot
- All authorized users share the same Taskwarrior data (single task database)
