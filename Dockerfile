FROM python:3.9.0

ADD bot.py /

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "./bot.py" ]
