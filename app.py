from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234Coolio"

boggle_game = Boggle()

@app.route("/")
def load_gameboard():
    """Create a boardgame and start a new session"""
    board = boggle_game.make_board()
    session['board'] = board

    #to allow highscore and number of plays to be saved
    num_plays = session.get("num_plays", 0)
    highscore = session.get("highscore", 0)

    return render_template("index.html", board=board, highscore=highscore, num_plays=num_plays)

@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    #print(f"Checking word: {word}, Result: {response}")
    return jsonify({'result': response})

@app.route("/score", methods=["POST"])
        #In a Flask application, request.json is used to parse JSON data from the incoming request. When a client sends data to the server using a POST request with the content type set to "application/json," the JSON data is typically included in the request body. The request.json attribute in Flask is a convenient way to access this JSON data.
def score_plays():
    """Receive score, update the number of times user played, and update the highscore if needed"""
    score = request.json["score"]
    # import pdb
    # pdb.set_trace()
    
    num_plays = session.get("num_plays", 0)
    highscore = session.get("highscore", 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord= score > highscore)