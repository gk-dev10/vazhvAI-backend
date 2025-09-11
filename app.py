from flask import Flask
from routes.authRoutes import authRoutes
from routes.productRoutes import productRoutes
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS for API routes
cors_config = {
    "resources": {
        r"/api/*": {
            "origins": "http://localhost:5173",  # Change this to your frontend origin
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        },
        r"/products/*": {
            "origins": "http://localhost:5173",  # Change this to your frontend origin
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        },
    },
    "expose_headers": ["Content-Type", "Authorization"],
}

cors_config["supports_credentials"] = True

CORS(app, **cors_config)
app.register_blueprint(authRoutes, url_prefix="/api")
app.register_blueprint(productRoutes, url_prefix="/products")

@app.route("/")
def home():
    return {"msg": "VazhvAI Backend running"}

if __name__ == "__main__":
    app.run(debug=True)