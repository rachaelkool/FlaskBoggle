from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"

boggle_game = Boggle()


@app.route('/')
def homepage():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    no_plays = session.get("no_plays", 0)

    return render_template("index.html", board=board, highscore=highscore, no_plays=no_plays)


@app.route('/check-word')
def check_word():
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})
   


@app.route("/post-score", methods=["GET", "POST"])
def post_score():
    if request.method == 'POST':
        score = request.json["score"]
        highscore = session.get("highscore", 0)
        nplays = session.get("nplays", 0)

        session['nplays'] = nplays + 1
        session['highscore'] = max(score, highscore)

        return jsonify(brokeRecord=score > highscore)
    else: 
        return