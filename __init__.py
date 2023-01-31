from flask import Flask, jsonify, request, abort
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)


db = SQLAlchemy(app)
ma = Marshmallow(app)  



from app import routes