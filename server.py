from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os, random, string


class Server():

    def __init__(self):
        self.clients = {}
        self.lobbies = {}
    
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

socketio = SocketIO(app)

