from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os, random, string
from data import DataStorage
from lobby import Lobby
from boardstate import BoardState
from player import Player


class Server():

    def __init__(self):
        self.clients = {}
        self.lobbies = {}
        self.DataStore = DataStorage("tileset.json")
    
    def handleJoin(self, Lobby, Player):
        pass

    def handleLeave(self, Lobby, Player):
        pass

    def handleUpdate(Lobby, Data):
        pass


app = Flask(__name__)
# First Time Crypto Setup Handler
if ".env" not in os.listdir():
    f = open(".env", "a")
    f.write(f"SECRET_KEY={''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}")
    f.close()

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app)
server = Server()

# Route to homepage
# Displays all currently running games with join button, current number of players, and creation timestamp
@app.route("/")
def home_view():
    return render_template('home.html', server=server, sid=session.sid)

# Route to bingo tile manager
# Displays all tiles and tilesets currently stored, and allows for the creation of new tiles and tilesets
@app.route("/tiles")
def tile_manager():
    return render_template('tiles.html', data=server.DataStore)

# Route to lobby create
# Displays interface for configuring and creating a new game
@app.route("/create", methods=["GET", "POST"])
def lobby_manager():
    if request.method == "POST":
        lobby_id = request.form['id']
        lobby_name = request.form['name']
        free_tile = request.form['freetile']
        for attr in request.form:
            if "-en" in attr:
                tileset = attr
        server.lobbies[lobby_id] = Lobby(lobby_name, lobby_id, tileset)
        return redirect(f"/lobby/{lobby_id}/{session.sid}")
    return render_template('create.html', server=server, id=''.join(random.choices(string.ascii_uppercase + string.digits, k=16)))

# Route to lobby manager
# Displays all boardstates and player information in given lobby
@app.route("/lobby/<lobby_id>/")
def lobby_view(lobby_id):
    return render_template("game.html", lobby_id=lobby_id, server=server, sid=session.sid)


# Route to game view
# Shows a player their board and interface for play
@app.route("/lobby/<lobby_id>/<player_id>")
def game_view(lobby_id, player_id):
    board_state: BoardState = BoardState(5)
    server.lobbies[lobby_id].players[str(player_id)] = Player(session.sid, session.sid, board_state)
    return render_template("game.html", lobby_id=lobby_id, player_id=player_id, board=board_state)

# Run the Flask application
if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port='8080')
    print("Started Server")

