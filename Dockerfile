
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --no-create-home appuser

COPY app/server.py /app/server.py
COPY app/index.html /app/index.html

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

CMD ["python", "/app/server.py"]
