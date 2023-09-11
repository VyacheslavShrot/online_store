FROM python:3.10

RUN apt update
RUN mkdir /store

WORKDIR /store

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY ./commands ./commands

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

CMD ["bash"]
