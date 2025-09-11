from flask import Flask
from routes.authRoutes import authRoutes
from routes.productRoutes import productRoutes
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/auth/*": {"origins": ["http://localhost:5173"],"supports_credentials": True,"allow_headers": ["Authorization", "Content-Type"],"methods": ["GET", "POST", "PATCH", "OPTIONS"]}})

app.register_blueprint(authRoutes, url_prefix="/api")
app.register_blueprint(productRoutes, url_prefix="/products")

@app.route("/")
def home():
    return {"msg": "VazhvAI Backend running"}

if __name__ == "__main__":
    app.run(debug=True)