from Player import Player
from Costum_Exceptions import MissingPlayerError

class Player_List():
    def __init__(self, player_list = []):
        self.player_list = player_list

    @classmethod
    def from_json(cls, j):
        player_list = [Player.from_json(pj) for pj in j]
        return cls(player_list)

    def add_player(self, player: Player):
        self.player_list.append(player)

    def get_player_by_name(self, name):
        for player in self:
            if name == player.name: return player
        raise MissingPlayerError(f"Player {name} not found.")
        return None

    def is_player(self, name):
        for player in self.player_list:
            if name == player.name: return True
        return False

    def sorted(self):
        self.player_list.sort(key = lambda player: player.rating, reverse = True)
        return self

    def __iter__(self): yield from self.player_list
    def __len__(self):  return len(self.player_list)

    def __eq__(self, other):
        if self.name == other.name: return True
        return False

    def to_json(self):  return [player.to_json() for player in self.player_list]
    def __repr__(self): return ",\n".join(repr(player) for player in self.player_list)
    def __str__(self):  return ",\n".join(str(player) for player in self.player_list)