import os

from flask import Flask

from src.api.routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    # En producción se usa gunicorn (ver Dockerfile); esto es solo para desarrollo local.
    app.run(host=os.getenv("FLASK_HOST", "127.0.0.1"),
            port=int(os.getenv("PORT", "5000")),
            debug=os.getenv("FLASK_DEBUG") == "1")
