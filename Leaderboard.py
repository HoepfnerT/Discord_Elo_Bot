from Player_List import Player_List
from Result_List import Result_List
from Player import Player
from Result import Result, Score
from Costum_Exceptions import PlayerCreationError
import random


class Leaderboard():
    def __init__(self, player_list = Player_List(), result_list = Result_List(), rating_period = 0):
        self.player_list    = player_list
        self.result_list    = result_list
        self.rating_period  = rating_period

    @classmethod
    def from_json(cls, j):
        rating_period       = j["Rating_Period"]
        player_list         = Player_List.from_json(j["Players"])
        result_list         = j["Pending"]
        if len(result_list) > 0:
            for result in result_list:
                result["Payload"]["Player1"] = player_list.get_player_by_name(result["Payload"]["Player1"])
                result["Payload"]["Player2"] = player_list.get_player_by_name(result["Payload"]["Player2"])
        result_list = Result_List.from_json(j["Pending"])
        return cls(player_list, result_list, rating_period)


    def add_player(self, player: Player, creator = "Not Available"):
        if player in self.player_list: 
            raise PlayerCreationError("A player with that name already exists.")
        self.player_list.add_player(player)

    def add_player_by_name(self, name, creator = "Not Available"):
        player = Player(name, creator = creator)
        self.add_player(player)

    def add_players(self, players):
        for player in players: self.add_player(player)

    def add_result(self, result: Result):
        self.result_list.add_result(result)

    def remove_result(self, result: Result):
        return self.result_list.delete_result(result)

    def add_result_by_names(self, name1, name2, score1, score2, submitter, time, channel):
        player1 = self.get_player_by_name(name1)
        player2 = self.get_player_by_name(name2)
        self.add_result(Result(submitter, time, channel, player1, player2, Score(score1, score2)))

        
    def remove_result_by_names(self, name1, name2, score1, score2, submitter, time, channel):
        player1 = self.get_player_by_name(name1)
        player2 = self.get_player_by_name(name2)
        return self.remove_result(Result(submitter, time, channel, player1, player2, Score(score1, score2)))

    def add_results(self, results):
        for result in results: 
            print(result)

    def clear_result_list(self, increment_rating_period = True):
        self.rating_period += 1
        self.result_list.clear()

    def is_player(self, name):
        return self.player_list.is_player(name)

    def get_player_list(self):      return self.player_list
    def get_result_list(self):      return self.result_list

    def get_player_by_name(self, name):
        return self.player_list.get_player_by_name(name)


    def get_standing(self, min_games=10, inactive_threshhold=3):
        active_list = [player for player in self.player_list.sorted()  if player.inactive < inactive_threshhold and player.games >= min_games]
        inactive_list = [player for player in self.player_list.sorted()  if player.inactive >= inactive_threshhold and player.games >= min_games]
        new_list = sorted([player for player in self.player_list  if player.games < min_games], key=lambda pl: str(pl))
        out = "\n".join(f"{i+1}: {player} ({round(player.rating)})" for i, player in enumerate(active_list)) + (len(active_list)>0) * "\n"
        out += "\n".join(f"%: {player} ({round(player.rating)}?)" for i, player in enumerate(inactive_list)) + (len(inactive_list)>0) * "\n"
        out += "\n".join(f"%: {player} (???)" for i, player in enumerate(new_list))
        return out

    def get_pending_str(self):
        return "Pending:\n" + f"{self.result_list}"
    def to_json(self):
        return {"Rating_Period": self.rating_period, "Players": self.player_list.to_json(), "Pending": self.result_list.to_json()}
    def __repr__(self):
        return f"Participating players: \n{repr(self.player_list)} \n\nPeding results: \n{repr(self.result_list)}."
    def __str__(self):
        return "\n".join(f"{i+1}: {player} ({round(player.rating)})" for i, player in enumerate(self.player_list.sorted()))
