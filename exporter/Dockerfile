FROM python:3.11-slim

WORKDIR /exporter

COPY exporter.py .

RUN pip install oci prometheus_client

EXPOSE 8080

CMD ["python", "exporter.py"]