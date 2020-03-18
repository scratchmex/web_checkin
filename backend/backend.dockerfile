FROM tiangolo/uvicorn-gunicorn:python3.7

RUN rm -rf /app/app
ENV PYTHONPATH=/app

COPY . /app
WORKDIR /app

ENV APP_MODULE api:app
RUN pip install pipenv
RUN pipenv install --system --deploy

EXPOSE 80
