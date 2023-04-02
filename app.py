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
import nltk
from nltk.corpus import stopwords
from gensim import corpora, models
import re
import openai
from flask import Flask, redirect, render_template, request, url_for
from gtts import gTTS

nltk.download('punkt')
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

result = ' '
matches = ''


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        words = request.form["words"]
        prompt = generate_prompt(words)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            temperature=1,
        )
        global result
        result = response.choices[0].text
        # Tokenize the poem and remove punctuation marks
        tokens = nltk.word_tokenize(result)
        tokens = [token for token in tokens if token.isalpha()]

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token.lower() not in stop_words]

        # Create a bag-of-words representation
        dictionary = corpora.Dictionary([tokens])
        corpus = [dictionary.doc2bow(tokens)]

        # Build the LDA model
        lda_model = models.LdaModel(corpus=corpus,
                                    id2word=dictionary,
                                    num_topics=1,
                                    passes=50,
                                    alpha='auto',
                                    per_word_topics=True)

        # Extract the themes
        theme = lda_model.show_topics()[0][1]
        pattern = r'"([^"]*)"'
        global matches
        matches = re.findall(pattern, theme)
        print(matches)
        myobj = gTTS(text=result, lang='en', slow=False)
        myobj.save("static/poem.mp3")
        return redirect(url_for("index", result=result))
    response2 = openai.Image.create(
        prompt="low quality image with following themes:\n" + str(matches),
        n=1,
        size="256x256"
    )
    result = request.args.get("result")
    result2 = response2['data'][0]['url']
    return render_template("index.html", result=result, image_url=result2)


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
