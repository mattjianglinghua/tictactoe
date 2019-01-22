from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from copy import deepcopy

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def switch():
    """Switches whose turn it is."""
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"         
    return redirect(url_for("index"))

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None
        session["history"] = []

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=session["winner"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    """Marks board, stores move into history, continues or ends game."""

    #mark board
    session["board"][row][col] = session["turn"]

    #store move into history
    session["history"].insert(0, (row, col))
    print(session["history"])
      
    #current states
    board = session["board"]
    turn = session["turn"]

    def gamestatus():
        """Returns 1 if a winner, 0 if tie, -1 if still playing."""

        #check rows
        for row in session["board"]:
            if turn == row[0] == row[1] == row[2]:
                return 1
        #check columns
        for col in range(3):
            if turn == session["board"][0][col] == session["board"][1][col] == session["board"][2][col]:
                return 1
        #check diagonals 
        if turn == session["board"][0][0] == session["board"][1][1] == session["board"][2][2] or turn == session["board"][0][2] == session["board"][1][1] == session["board"][2][0]:
            return 1

        #if it's not a tie
        for row in board:
            for cell in row:
                if cell == None:
                    return -1
        #otherwise if it's a tie
        session["tie"] = True
        return 0

    #check game status
    if gamestatus() == 1:
        session["winner"] = turn
        return redirect(url_for("index"))
    elif gamestatus() == 0:
        session["winner"] = "tie"
        return redirect(url_for("index"))
    else:
        if session["turn"] == "X":
            session["turn"] = "O"
        else:
            session["turn"] = "X"         
        return redirect(url_for("index"))

@app.route("/reset")
def reset():
    """Resets board and session variables."""

    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["winner"] = None
    session["history"].clear()
    session["turn"] = "X"
    return redirect(url_for("index"))

@app.route("/undo")
def undo():
    """Undo previous moves and switches turn."""

    move = session["history"].pop(0)
    session["board"][move[0]][move[1]] = None

    #switch turns
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"         
    return redirect(url_for("index"))    


    