from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

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
        session["history"] = []

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=session["winner"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    #mark board and add previous board to history
    session["history"].append(session["board"])
    #print(session["history"])
    session["board"][row][col] = session["turn"]
  
    #current states
    board = session["board"]
    turn = session["turn"]

    #function to check for winner
    def gameover():
        #check rows
        for row in board:
            if turn == row[0] == row[1] == row[2]:
                return True
        #check columns
        for col in range(3):
            if turn == board[0][col] == board[1][col] == board[2][col]:
                return True
        #check diagonals 
        if turn == board[0][0] == board[1][1] == board[2][2] or turn == board[0][2] == board[1][1] == board[2][0]:
            return True

        #check if board is completely filled yet
        for row in board:
            for cell in row:
                if cell == None:
                    return False

        #otherwise if it's a tie
        return True

    #display game over if it's over...
    if gameover():
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


