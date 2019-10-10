# FROM python:3-slim
FROM python:2-slim

WORKDIR /dogmover
COPY . /dogmover

RUN pip install -r requirements.txt --upgrade

RUN chmod +x dogmover.py

ENTRYPOINT ["./dogmover.py"]

