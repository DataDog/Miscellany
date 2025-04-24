FROM datadog/agent:latest

COPY src/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY /src /app
WORKDIR /app

CMD ["python3", "collect_configs.py"]