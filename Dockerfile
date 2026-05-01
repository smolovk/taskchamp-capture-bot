FROM python:3.11-slim

# Install Taskwarrior and dependencies
RUN apt-get update && apt-get install -y \
    taskwarrior \
    taskwarrior-data \
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
