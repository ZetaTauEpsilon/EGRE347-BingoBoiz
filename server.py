from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit    
from dotenv import load_dotenv
import os, random, string
from data import DataStorage
from lobby import Lobby
from boardstate import BoardState
from player import Player
import json


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
        size = request.form['size']
        if 'freetile' in request.form:
            free_tile = True
        else:
            free_tile = False
        for attr in request.form:
            if "-en" in attr:
                tileset = attr.replace("-en", "")
        server.lobbies[lobby_id] = Lobby(lobby_name, lobby_id, server.DataStore.TileSets[tileset], int(size), free_tile)
        session["lobby_id"] = lobby_id
        session["sid"] = session.sid
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
    session["lobby_id"] = lobby_id
    session["sid"] = session.sid
    lobby = server.lobbies[lobby_id]
    if player_id not in lobby.players:
        lobby.players[str(player_id)] = Player(session.sid, session.sid, lobby.GameManager.makeBoard(lobby, lobby.tileset, lobby.free, lobby.size))
    return render_template("game.html", lobby_id=lobby_id, player_id=player_id, board=lobby.players[str(player_id)].board)

@socketio.on('join')
def on_join(data):
    print("join")
    join_room(session['lobby_id'])
    player = server.lobbies[session['lobby_id']].players[session['sid']]
    emit("refresh", {"player_id": session['sid'], "name": player.name, "states": server.lobbies[session['lobby_id']].players[session['sid']].board.state}, room=request.sid, json=True)
    emit("state_update", {"player_id": session['sid'], "name": player.name, "states": server.lobbies[session['lobby_id']].players[session['sid']].board.state}, room=session['lobby_id'], json=True)
    for player in server.lobbies[session['lobby_id']].players:
        if player != session['sid']:
            emit("state_update", {"player_id": player, "name": server.lobbies[session['lobby_id']].players[player].name, "states": server.lobbies[session['lobby_id']].players[player].board.state}, room=session['lobby_id'], json=True)

@socketio.on('state_update')
def on_update(data):
    print("state_update")
    print(data)
    player = server.lobbies[session['lobby_id']].players[session['sid']]
    server.lobbies[session['lobby_id']].players[session['sid']].board.updateState(int(data['y'])-1, int(data['x'])-1)
    emit("state_update", {"player_id": session['sid'], "name": player.name, "states": server.lobbies[session['lobby_id']].players[session['sid']].board.state}, room=session['lobby_id'], json=True)

@socketio.on('rename')
def on_rename(data):
    print("rename")
    player = server.lobbies[session['lobby_id']].players[session['sid']]
    player.name = data['name']
    emit("state_update", {"player_id": session['sid'], "name": player.name, "states": server.lobbies[session['lobby_id']].players[session['sid']].board.state}, room=session['lobby_id'], json=True)

# Run the Flask application
if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port='8080')
    print("Started Server")

