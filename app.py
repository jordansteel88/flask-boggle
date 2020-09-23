from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


boggle_game = Boggle()


@app.route('/')
def home():
    """Show homepage."""
    board = boggle_game.make_board()
    session['board'] = board

    record = session.get('record', 0)
    plays = session.get('plays', 0)

    return render_template('index.html', board=board, record=record, plays=plays)


@app.route('/submit-guess')
def handle_guess():
    """Receive guess from form and check validity."""
    guess = request.args['guess']
    board = session['board']
    res = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': res})



@app.route('/track-score', methods=["POST"])
def track_score():
    """Update score/play stats and send high score state response to js."""
    score = request.json['score']
    record = session.get('record', 0)
    plays = session.get('plays', 0)

    session['plays'] = plays + 1

    if score > record:
        session['record'] = score
        return jsonify(newRecord = True)

    return jsonify(newRecord = False)


