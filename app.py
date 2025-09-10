from flask import Flask
from routes.authRoutes import authRoutes

app = Flask(__name__)

app.register_blueprint(authRoutes, url_prefix="/api")

@app.route("/")
def home():
    return {"msg": "VazhvAI Backend running"}

if __name__ == "__main__":
    app.run(debug=True)
