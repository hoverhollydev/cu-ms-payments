#!/usr/bin/env python3
"""
API simple que responde Hola Mundo en el puerto 3000.
"""
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hola Mundo cu-ms-payments", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=False)