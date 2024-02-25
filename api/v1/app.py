#!/usr/bin/python3
"""App"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Docs"""
    return storage.close()


@app.errorhandler(404)
def notfound(error):
    """Docs"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
