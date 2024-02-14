FROM        python:3.10-bullseye
ENV         PYTHONUNBUFFERED 1
WORKDIR     /API/
COPY        . .
RUN         pip install -r requirements.txt
EXPOSE      9090
ENTRYPOINT  [ "python", "main.py"]
