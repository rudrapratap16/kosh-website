from flask import Flask
from routes.data_routes import data_bp
from config import BACKEND_PORT

def create_app():
    app = Flask(__name__)
    app.register_blueprint(data_bp, url_prefix="/api")
    return app

if __name__ == "__main__":
    app = create_app()
    print(f"✅ Flask running on http://127.0.0.1:{BACKEND_PORT}")
    app.run(debug=True, port=BACKEND_PORT)
