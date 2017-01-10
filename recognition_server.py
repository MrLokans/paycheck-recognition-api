from flask import (
    Flask,
    jsonify
)

app = Flask(__name__)


@app.route('/')
def recognize():
    return jsonify({"status": "working"})
