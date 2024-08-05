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

# Leer el archivo Excel
def read_excel():
    df = pd.read_excel('/mnt/data/data.xlsx', sheet_name='Sheet1')
    return df.to_dict(orient='records')

# Definir los tipos GraphQL
class CSVRow(ObjectType):
    id_tie_fecha_valor = String()
    id_cli_cliente = String()
    id_ga_vista = String()
    id_ga_tipo_dispositivo = String()
    id_ga_fuente_medio = String()
    desc_ga_sku_producto = String()
    desc_ga_categoria_producto = String()
    fc_agregado_carrito_cant = String()  # Cambié a String para mantener consistencia
    fc_ingreso_producto_monto = String()  # Cambié a String para mantener consistencia
    fc_retirado_carrito_cant = String()  # Cambié a String para mantener consistencia
    fc_detalle_producto_cant = String()  # Cambié a String para mantener consistencia
    fc_producto_cant = String()  # Cambié a String para mantener consistencia
    desc_ga_nombre_producto = String()
    fc_visualizaciones_pag_cant = String()  # Cambié a String para mantener consistencia
    flag_pipol = String()
    SASASA = String()
    id_ga_producto = String()
    desc_ga_nombre_producto_1 = String()
    desc_ga_sku_producto_1 = String()
    desc_ga_marca_producto = String()
    desc_ga_cod_producto = String()
    desc_categoria_producto = String()
    desc_categoria_prod_principal = String()

# Definir el tipo de dato basado en las columnas del Excel
class DataType(graphene.ObjectType):
    id_tie_fecha_valor = graphene.String()
    id_cli_cliente = graphene.String()
    id_ga_vista = graphene.String()
    id_ga_tipo_dispositivo = graphene.String()
    id_ga_fuente_medio = graphene.String()
    desc_ga_sku_producto = graphene.String()
    desc_ga_categoria_producto = graphene.String()
    fc_agregado_carrito_cant = graphene.Float()
    fc_ingreso_producto_monto = graphene.Float()
    fc_retirado_carrito_cant = graphene.Float()
    fc_detalle_producto_cant = graphene.Float()
    fc_producto_cant = graphene.Float()
    desc_ga_nombre_producto = graphene.String()
    fc_visualizaciones_pag_cant = graphene.Float()
    flag_pipol = graphene.String()
    SASASA = graphene.String()
    id_ga_producto = graphene.String()
    desc_ga_nombre_producto_1 = graphene.String()
    desc_ga_sku_producto_1 = graphene.String()
    desc_ga_marca_producto = graphene.String()
    desc_ga_cod_producto = graphene.String()
    desc_categoria_producto = graphene.String()
    desc_categoria_prod_principal = graphene.String()

class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    getData = String()
    getAllRows = List(CSVRow)
    getRowByColumnValue = Field(CSVRow, column_name=String(), value=String())
    all_data = List(DataType)

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

    def resolve_all_data(self, info):
        data = read_excel()
        return [DataType(**item) for item in data]

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
