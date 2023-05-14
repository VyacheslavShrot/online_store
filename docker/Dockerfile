FROM python:3.10

RUN apt update
RUN python --version

RUN mkdir /docker
WORKDIR /docker

COPY pyfile_for_docker.py ./pyfile_for_docker.py
COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

CMD ["python", "pyfile_for_docker.py"]


