FROM python:3.8
WORKDIR /Project/ml-apple

COPY requirements.txt ./

RUN apt-get update && apt-get install python3-pip -y
RUN pip3 install pip -U
RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip3 config set install.trusted-host mirrors.aliyun.com
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "image_server:app", "-c", "./gun_config.py"]
