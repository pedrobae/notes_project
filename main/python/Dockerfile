FROM python:3.10.12

ADD requirements.txt /temp

RUN python -m pip install -r /tmp/requirements.txt

WORKDIR /home

EXPOSE 8000
CMD ["python", "0.0.0.0:8000"]
