FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY *.py ./
RUN mkdir ./cache ./output

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./index.py" ]