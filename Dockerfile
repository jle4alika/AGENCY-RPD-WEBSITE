FROM python:3.10-slim

WORKDIR /

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

expose 5000

CMD ["python", "app.py"]