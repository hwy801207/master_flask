from flask import Flask, current_app
from config import DevConfig;
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user_" 
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)

@app.route("/", methods=["GET"])
def index():
    return "index home page";

if __name__ == '__main__':
    app.run()
