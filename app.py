
from src import app
from src.routes.funcionarios.index import *
from src.routes.categorias.index import *
from src.routes.produtos.index import *

@app.route('/')
def home():
    return"<p>Ok</p>"


if __name__ == '__main__':
    app.run(debug=True)