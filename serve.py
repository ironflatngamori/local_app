#!/usr/bin/env python
from views import app_views
from flask import Flask, jsonify
from config import __PORT__

app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def page_not_found(_):
    """
    if the route is not found return an error
    """
    return (jsonify({"error": "Resource Not found"}), 404)


if __name__ == '__main__':
    app.run(debug=True, port=__PORT__)
