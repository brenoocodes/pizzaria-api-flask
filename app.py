
from src import app
from src.routes.funcionarios.index import *

@app.route('/')
def home():
    return"<p>Ok</p>"


if __name__ == '__main__':
    app.run(debug=True)