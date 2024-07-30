# Dockerfile

FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Instalar el modelo de Spacy
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["python", "src/main.py"]