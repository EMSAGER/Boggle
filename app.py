from boggle import Boggle
from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234Coolio'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.route('/')
def load_gameboard():
    """Create boardgame & start a new session for the game plays"""
    board = boggle_game.make_board()
    session['board'] = boggle_game
    return render_template('index.html', board=board)