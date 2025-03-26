from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/', methods=['GET'])
def index():
    """
    A simple endpoint that returns a greeting.
    ---
    responses:
      200:
        description: A greeting message
        content:
          text/html:
            schema:
              type: string
              example: "<p>Hello, World!</p>"
    """
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(
        "0.0.0.0",
        8000,
        debug=True
    )