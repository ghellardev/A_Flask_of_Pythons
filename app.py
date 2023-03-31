# from flask import Flask, redirect, url_for
# import socket
# import pymongo
#
# app = Flask(__name__)
#
# client = pymongo.MongoClient('_')  # mongodb://localhost:27017/
# db = client['__']  # replace with your database name
# collection = db['___']  # replace with your collection name
#
#
# @app.route("/hostname/")
# def return_hostname():
#     return f"{socket.gethostname()}"
#
#
# @app.route("/")
# def return_to_home():
#     return redirect(url_for('return_hostname'))
#
#

#
#
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# @app.errorhandler(418)
# def catch_all(path):
#     return "I'm a teapot.", 418
#
#
# if __name__ == '__main__':
#     app.run()
import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        words = request.form["words"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(words),
            max_tokens=256,
            temperature=1,
        )
        result = response.choices[0].text
        print(result)
        return redirect(url_for("index", result=result))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(words):
    # return """Generate a 5 line poem using the words from this list {}
    # first line should be the title  which should not contain the words from the list followed by 3 empty lines
    # """.format(
    #     words.capitalize()
    return """Generate a 5 line poem using the words from this list {}
         first line should be the title  which should not contain the words from the list followed by 3 empty lines
         """.format(
             words.capitalize()
    )

