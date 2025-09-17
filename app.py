from flask import Flask
from models import db
from config import Config
import firebase_admin
from firebase_admin import credentials
from routes import api

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Firebase initialization
cred = credentials.Certificate(Config.FIREBASE_CERT_PATH)
firebase_admin.initialize_app(cred)

# Register blueprint
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
