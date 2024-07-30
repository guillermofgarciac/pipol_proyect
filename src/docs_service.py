from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/graphql')
def graphql_doc():
    """
    GraphQL Endpoint
    ---
    get:
      description: Obtiene datos del CSV usando GraphQL
      responses:
        200:
          description: Datos en formato GraphQL
    """
    pass

@app.route('/nlp', methods=['POST'])
def nlp_doc():
    """
    NLP Endpoint
    ---
    post:
      description: Consulta datos del CSV usando lenguaje natural
      responses:
        200:
          description: Resultados de la consulta en lenguaje natural
    """
    pass

if __name__ == '__main__':
    app.run(debug=True)
