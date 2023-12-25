from flask import Flask, request, render_template, jsonify, session, flash
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234Coolio"

boggle_game = Boggle()

@app.route("/")
def load_gameboard():
    """Create a boardgame and start a new session"""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template("index.html", board=board)

@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    print(f"Checking word: {word}, Result: {response}")
    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
