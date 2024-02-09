FROM        python:3.10-bullseye
ENV         PYTHONUNBUFFERED 1
WORKDIR     /API/
COPY        . .
# add requirements
# RUN         pip install -r requirements.txt
# EXPOSE      ...
ENTRYPOINT  [ "python", "main.py"]
