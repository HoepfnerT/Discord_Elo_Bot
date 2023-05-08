import glicko2
import Player, Result
import Leaderboard

class Rating():
    def __init__(self, rating=1500, rd=350, vol=0.06):
        self.rating     = rating
        self.rd         = rd
        self.vol        = vol

    @classmethod
    def from_json(cls, j):
        rating = j["rating"]
        rd = j["rd"]
        vol = j["vol"]
        return cls(rating, rd, vol)

    def to_glicko(self):
        return glicko2.Player(self.rating, self.rd, self.vol)

    def get_display_rating(self): 
        return self.rating - self.rd

    def __round__(self, digits=0):
        if digits == 0: return int(self.get_display_rating())
        return round(self.get_display_rating(), digits)

    ## Dunder methods to compare ratings
    def __eq__(self, other):    return (self.get_display_rating() == other.get_display_rating()) and (self.rd == other.rd)
    def __gt__(self, other):    return (self.get_display_rating() > other.get_display_rating()) or (self.get_display_rating() == other.get_display_rating() and self.rd < other.rd)
    def __lt__(self, other):    return other > self
    def __ge__(self, other):    return self == other or self > other
    def __le__(self, other):    return other >= self

    def to_json(self): return {"rating": self.rating, "rd": self.rd, "vol": self.vol}
    def __str__(self): return f"{round(self)}"


# Resolve all open results of a Leaderboard
def resolve_result_list(leaderboard: Leaderboard):
    result_list = leaderboard.get_result_list()
    for player in leaderboard.get_player_list():
        glicko_player = player.get_rating().to_glicko()
        game_list = [result.glickofy(player) for result in result_list if result.contains(player)]
        if len(game_list) == 0: 
            glicko_player.did_not_compete()
            rating, rd, vol = glicko_player.get_rating_vals()
            player.update_rating(Rating(rating, rd, vol), False)
        else:
            rating_list, RD_list, outcome_list = tuple(map(list, zip(*game_list)))
            glicko_player.update_player(rating_list, RD_list, outcome_list)
            rating, rd, vol = glicko_player.get_rating_vals()
            player.update_rating(Rating(rating, rd, vol), True, number_of_games = len(game_list))
    leaderboard.clear_result_list()
