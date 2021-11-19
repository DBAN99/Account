
FROM python:3.9

LABEL maintainer="dban7171@gmail.com"

COPY . /app/server

WORKDIR /app/server

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]

EXPOSE 8000