# Build and push command (run from repo root):
# docker build -t docker.s1ngle.xyz/taskchamp-bot:latest . && docker push docker.s1ngle.xyz/taskchamp-bot:latest
#
# Or with buildx for multi-arch:
# docker buildx build --platform linux/amd64,linux/arm64 -t docker.s1ngle.xyz/taskchamp-bot:latest --push .

FROM python:3.11-slim

# Install Taskwarrior
RUN apt-get update && apt-get install -y \
    taskwarrior \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create task data directory
RUN mkdir -p /root/.task

# Set environment
ENV PYTHONUNBUFFERED=1
ENV TASKRC_PATH=/root/.taskrc
ENV TASK_DATA_DIR=/root/.task

# Run the bot
CMD ["python", "-m", "src.bot"]
