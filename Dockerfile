FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl ffmpeg wget bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Render supplies PORT at runtime. app.py reads it automatically.
EXPOSE 10000

CMD ["python", "render_start.py"]
