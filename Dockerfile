FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /api
WORKDIR /api

CMD python db_models.py
CMD uvicorn app:app --reload