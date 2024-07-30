from flask import Flask, request, jsonify
import pandas as pd
import spacy

# Cargar datos del CSV
data = pd.read_csv('data/data.csv')
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

@app.route('/nlp', methods=['POST'])
def nlp_query():
    query = request.json.get('query')
    doc = nlp(query)
    # Procesar la consulta y devolver los resultados apropiados
    # Esto es solo un ejemplo simple
    results = data.to_dict(orient='records')
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
