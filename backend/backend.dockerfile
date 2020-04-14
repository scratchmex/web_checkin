FROM tiangolo/uvicorn-gunicorn:python3.7

RUN rm -rf /app/app

ENV PIP_NO_CACHE_DIR=false
ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system --deploy

COPY . .

ENV APP_MODULE api:app

EXPOSE 80
