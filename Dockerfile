
# FROM ubuntu:14.04
# LABEL maintainer="dban7171@gmail.com"
#
# RUN sudo apt-get update
# RUN sudo apt-get install mysql-server-5.7
# RUN 스키마 셋업
#
# RUN 파이썬 설치
#
#
# COPY . /app/server
#
# WORKDIR /app/server
#
# RUN pip install -r requirements.txt
#
# ENTRYPOINT ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
#
# EXPOSE 8000