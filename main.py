from server import socketio, app
from flask import render_template
from data import DataStorage
from server import Server
from boardstate import BoardState

data_: DataStorage = DataStorage()
server_: Server = Server()


# Route to homepage
# Displays all currently running games with join button, current number of players, and creation timestamp
@app.route("/")
def home_view():
    return render_template('home.html', server=server_)

# Route to bingo tile manager
# Displays all tiles and tilesets currently stored, and allows for the creation of new tiles and tilesets
@app.route("/tiles")
def tile_manager():
    return render_template('tiles.html', data=data_)

# Route to lobby create
# Displays interface for configuring and creating a new game
@app.route("/create")
def lobby_manager():
    return render_template('create.html', server=server_)

# Route to lobby manager
# Displays all boardstates and player information in given lobby
@app.route("/lobby/<lobby_id>")
def lobby_view(lobby_id):
    return render_template("lobby.html", lobby_id=lobby_id, server=server_)


# Route to game view
# Shows a player their board and interface for play
@app.route("/lobby/<lobby_id>/<player_id>")
def game_view(lobby_id, player_id):
    if player_id not in server_.lobbies[lobby_id].players:
        server_.lobbies[lobby_id].addPlayer(player_id)
    board_state: BoardState = BoardState()
    return render_template("game.html", lobby_id=lobby_id, player_id=player_id, board_state=board_state)

# Run the Flask application
if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port='8080')
    print("Started Server")