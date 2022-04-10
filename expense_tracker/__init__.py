from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__) 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///joey.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ouvszwdwtrpvio:7ca1c2e84226603f7ddcbda2c41caa4f1fc61a1535864ed7c11b23bc3db55c64@ec2-52-203-118-49.compute-1.amazonaws.com:5432/ddhul1vt45jme2'
app.config['SECRET_KEY'] = "as#asdASASF#ASFLKsndvssdf2p2990$"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from expense_tracker import routes
