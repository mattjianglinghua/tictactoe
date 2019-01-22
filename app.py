from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from copy import deepcopy

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None
        session["tie"] = False
        session["history"] = []

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=session["winner"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    #mark board and add previous board to history
    board = deepcopy(session["board"])
    print(board)
    session["history"].append(board)
    print(session["history"])
    session["board"][row][col] = session["turn"]
  
    #current states
    
    turn = session["turn"]

    #function to check for winner
    def gameover():
        #check rows
        for row in session["board"]:
            if turn == row[0] == row[1] == row[2]:
                return True
        #check columns
        for col in range(3):
            if turn == session["board"][0][col] == session["board"][1][col] == session["board"][2][col]:
                return True
        #check diagonals 
        if turn == session["board"][0][0] == session["board"][1][1] == session["board"][2][2] or turn == session["board"][0][2] == session["board"][1][1] == session["board"][2][0]:
            return True

        #check if board is completely filled yet
        for row in board:
            for cell in row:
                if cell == None:
                    return False

        #otherwise if it's a tie
        session["tie"] = True
        return True
    #display game over if it's over...
    if gameover():
        if session["tie"]:
            session["winner"] = "tie"
        else:
            session["winner"] = turn
        return redirect(url_for("index"))

    #...otherwise change turns
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
            
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["winner"] = None
    return redirect(url_for("index"))

    