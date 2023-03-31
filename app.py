from flask import Flask, redirect, url_for
import socket
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient('_')  # mongodb://localhost:27017/
db = client['__']  # replace with your database name
collection = db['___']  # replace with your collection name


@app.route("/hostname/")
def return_hostname():
    return f"{socket.gethostname()}"


@app.route("/")
def return_to_home():
    return redirect(url_for('return_hostname'))


@app.route("/oldhostname/")
def return_oldhost():
    return redirect(url_for('return_hostname'))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@app.errorhandler(418)
def catch_all(path):
    return "I'm a teapot.", 418


if __name__ == '__main__':
    app.run()
