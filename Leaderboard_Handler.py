from Leaderboard import Leaderboard
import Glicko_Handler
import json, copy
from Costum_Exceptions import PlayerCreationError, MissingPlayerError
from datetime import datetime


class Leaderboard_Handler():
    def __init__(self, leaderboard = Leaderboard(), filepath = ""):
        self.leaderboard    = leaderboard
        self.filepath       = filepath

    @classmethod
    def from_file(cls, file, filepath = ""):
        try:
            with open(file, "r") as f:
                j = json.load(f)
            return cls(Leaderboard.from_json(j), filepath = filepath)
        except Exception as e:
            print("Could not load Leaderboard from file.")
            print(e)
            return cls(filepath = filepath)
         



    def add_player(self, name, creator = "Not Available"):
        try:    self.leaderboard.add_player_by_name(name, creator = creator)
        except PlayerCreationError as e:    print(e)

    def is_player(self, name):
        return self.leaderboard.is_player(name)

    def add_result(self, name1, name2, score1, score2, submitter = "Not Available", time = "Not Available", channel="Not Available"):
        try:    self.leaderboard.add_result_by_names(name1, name2, score1, score2, submitter, time, channel)
        except MissingPlayerError as e:     print(e)

    def remove_result(self, name1, name2, score1, score2, submitter = "Not Available", time = "Not Available", channel="Not Available"):
        try:    return self.leaderboard.remove_result_by_names(name1, name2, score1, score2, submitter, time, channel)
        except MissingPlayerError as e:     print(e)

    def clear_results(self):
        try:    return self.leaderboard.clear_result_list(increment_rating_period = False)
        except MissingPlayerError as e:     print(e)

    def to_file(self, filename = f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}_save.json"):
        with open(self.filepath + filename, "w+") as f:
            json.dump(self.leaderboard.to_json(), f, indent=2)

    def resolve_results(self):
        self.to_file(filename = f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}_precommit.json")
        Glicko_Handler.resolve_result_list(self.leaderboard)
        self.to_file()

        
    def get_ranking(self, min_games=10, inactive_threshhold=3):
        return self.leaderboard.get_standing(min_games=min_games, inactive_threshhold=inactive_threshhold)

    def get_prediction(self, min_games=10, inactive_threshhold=3):
        prediction = copy.deepcopy(self.leaderboard)
        Glicko_Handler.resolve_result_list(prediction)
        return prediction.get_standing(min_games=min_games, inactive_threshhold=inactive_threshhold)

    def get_pending(self):
        return self.leaderboard.get_pending_str()

    def __str__(self):  return str(self.leaderboard)
    def __repr__(self): return repr(self.leaderboard)