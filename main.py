from flask import Flask
from config import DevConfig;

app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route("/", methods=["GET"])
def index():
    return "index home page";

if __name__ == '__main__':
    app.run()
