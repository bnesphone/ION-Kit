# ION Kit - AI Development Studio
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy toolkit files
COPY requirements.txt .
COPY version.py .
COPY kit.py .
COPY scripts/ scripts/
COPY tools/ tools/
COPY .agent/ .agent/
COPY docs/ docs/
COPY tests/ tests/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies for code-tools
WORKDIR /app/tools/code-tools
RUN npm install && npm run build

# Back to root
WORKDIR /app

# Create volume mount points
VOLUME ["/workspace"]

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ION_KIT_VERSION=6.1.0

# Default command shows help
ENTRYPOINT ["python", "kit.py"]
CMD ["--help"]

# Usage examples:
# docker build -t ion-kit .
# docker run ion-kit check
# docker run -v $(pwd):/workspace ion-kit analyze /workspace
# docker run -it ion-kit setup
