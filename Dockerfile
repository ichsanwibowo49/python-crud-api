FROM python:3.11-slim

WORKDIR /app
COPY app.py .

ENV DATA_FILE=/var/lib/backend_data/messages.json
RUN mkdir -p /var/lib/backend_data
VOLUME ["/var/lib/backend_data"]

EXPOSE 5000
CMD ["python", "app.py"]