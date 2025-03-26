from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(
        "0.0.0.0",
        8000,
        debug=True
    )