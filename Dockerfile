FROM python:3.11

COPY Requirements.txt Requirements.txt
RUN pip install -r Requirements.txt

COPY . /app

WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]