from player import Player
import string, random
from gamemanager import GameManager

class Lobby:

    def __init__(self, name, id, tileset, size, free):
        self.name = name
        self.players = {}
        self.id = id
        self.tileset = tileset
        self.size = size
        self.GameManager = GameManager(self.size)
        self.free = free

    def addPlayer(self, player_id):
        self.players[player_id] = Player(player_id, player_id, self.GameManager.makeBoard(self, self.tileset, self.free, self.size))
