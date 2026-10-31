FROM python:3.11-slim

WORKDIR /app
COPY app.py .

ENV DATA_FILE=/var/lib/backend_data/messages.json
RUN mkdir -p /var/lib/backend_data
VOLUME ["/var/lib/backend_data"]

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)" || exit 1
CMD ["python", "app.py"]
