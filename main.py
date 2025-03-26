from flask import Flask
from flasgger import Swagger

from app.api.endpoints.image import router as image_bp
from app.api.endpoints.user import router as user_bp
from app.core.settings import config
from app.db.configs.connection import db

db.connect()
db.create_tables()

app = Flask(__name__)

swagger = Swagger(app)

app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER

app.register_blueprint(image_bp)
app.register_blueprint(user_bp)

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