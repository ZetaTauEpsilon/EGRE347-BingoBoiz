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
    
    def getPlayer(self, lobby_id, player_id):
        return self.lobbies[lobby_id].players[player_id]

    def handleUpdate(self, lobby_id, player_id, data):
        self.lobbies[lobby_id].players[player_id].board.updateState(int(data['x'])-1, int(data['y'])-1)
        player = self.getPlayer(lobby_id, player_id)
        win = self.lobbies[lobby_id].GameManager.evaluateWin(player.board, int(data['y'])-1, int(data['x'])-1)
        print(win)
        self.getPlayer(lobby_id, player_id).board.win = win
    
    def stateUpdate(self, lobby_id, player_id, event_type="state_update", to_all=True):
        to = lobby_id if to_all else player_id
        player = self.getPlayer(lobby_id, player_id)
        data =  {
                "player_id": player_id, 
                "name": player.name, 
                "states": self.lobbies[lobby_id].players[player_id].board.state,
                "win": player.board.win
                }
        emit(event_type, data, room=to, json=True)
    


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
        print(server.lobbies[lobby_id])
        session["lobby_id"] = lobby_id
        session["sid"] = session.sid
        return redirect(f"/lobby/{lobby_id}/{session.sid}")

    new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return render_template('create.html', server=server, id=new_id)

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
    server.stateUpdate(session['lobby_id'], session['sid'], to_all=False, event_type="refresh")
    server.stateUpdate(session['lobby_id'], session['sid'])
    for player in server.lobbies[session['lobby_id']].players.keys():
        if player != session['sid']:
            server.stateUpdate(session['lobby_id'], player)

@socketio.on('state_update')
def on_update(data):
    print("state_update")
    print(data)
    server.handleUpdate(session['lobby_id'], session['sid'], data)
    server.stateUpdate(session['lobby_id'], session['sid'])

@socketio.on('rename')
def on_rename(data):
    print("rename")
    player = server.getPlayer(session['lobby_id'], session['sid'])
    player.name = data['name']
    server.stateUpdate(session['lobby_id'], session['sid'])

# Run the Flask application
if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port='8080')
    print("Started Server")

