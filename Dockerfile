FROM python:3.10-slim

WORKDIR /app

# Rakibidda qalabka nidaamka iyo compiler-ka C++ ee lagama maarmaanka u ah pytgcalls iyo ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
