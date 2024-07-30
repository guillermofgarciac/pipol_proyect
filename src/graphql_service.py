from flask import Flask
from flask_graphql import GraphQLView
import graphene
import pandas as pd

# Cargar datos del CSV
data = pd.read_csv('data/data.csv')

# Definir el esquema de GraphQL
class Item(graphene.ObjectType):
    column1 = graphene.String()
    column2 = graphene.String()

class Query(graphene.ObjectType):
    items = graphene.List(Item)

    def resolve_items(root, info):
        return [Item(column1=row['column1'], column2=row['column2']) for _, row in data.iterrows()]

schema = graphene.Schema(query=Query)

app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
