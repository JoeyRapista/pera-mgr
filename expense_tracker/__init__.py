from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///joey.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xuizmjghhrjill:51769414f14626d2e5582b9cfeadbbc395eeebc52cdc216b9d3f68fe23950081@ec2-52-73-155-171.compute-1.amazonaws.com:5432/d2d7k8ttson55g'
app.config['SECRET_KEY'] = "as#asdASASF#ASFLKsndvssdf2p2990$"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from expense_tracker import routes
