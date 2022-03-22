from flask import Flask, render_template
from sorteo import *
app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def index():
    return render_template('index.html',  tablas=tablas, mostrar_sorteo=False)

@app.route('/sorteo', methods=("POST", "GET"))
def sorteo():
    grupos = sortear()
    return render_template('index.html',  tablas=tablas, mostrar_sorteo=True, grupos = grupos)

if __name__ == "__main__":
    app.run(debug=True)