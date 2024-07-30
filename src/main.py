# main.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import spacy
from flasgger import Swagger, swag_from
from flask_graphql import GraphQLView
import graphene
from graphene import ObjectType, String, Field, List

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Cargar el modelo de Spacy
nlp = spacy.load("en_core_web_sm")

# Cargar los datos del CSV
data_path = '/app/data/data.csv'
data = pd.read_csv(data_path)

# Definir los tipos GraphQL
class CSVRow(ObjectType):
    column1 = String()
    column2 = String()
    column3 = String()
    # Añade más columnas según sea necesario

class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    getData = String()
    getAllRows = List(CSVRow)
    getRowByColumnValue = Field(CSVRow, column_name=String(), value=String())

    def resolve_hello(self, info, name):
        return f"Hello, {name}!"

    def resolve_getData(self, info):
        first_row = data.head(1).to_dict(orient='records')[0]
        return str(first_row)

    def resolve_getAllRows(self, info):
        rows = data.to_dict(orient='records')
        return [CSVRow(**row) for row in rows]

    def resolve_getRowByColumnValue(self, info, column_name, value):
        row = data[data[column_name] == value].head(1).to_dict(orient='records')
        if row:
            return CSVRow(**row[0])
        return None

schema = graphene.Schema(query=Query)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/data-loop', methods=['GET'])
def data_loop():
    html_table = data.to_html()
    return html_table

@app.route('/nlp', methods=['POST'])
@swag_from({
    'summary': 'NLP Endpoint',
    'parameters': [
        {
            'name': 'text',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'Texto para procesar con NLP'
        }
    ],
    'responses': {
        '200': {
            'description': 'Procesamiento NLP exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'tokens': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        }
                    }
                }
            }
        }
    }
})
def nlp_endpoint():
    text = request.json.get('text')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    return jsonify(tokens=tokens)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
