from Glicko_Handler import Rating
import re


class Player():
    def __init__(self, name, rating = Rating(), delta_rating = 0, inactive = 0, games_played = 0, creator = "Not Available"):
        self.name           = re.sub(r"\s+", r"", name)
        self.rating         = rating
        self.delta_rating   = delta_rating
        self.inactive       = inactive
        self.games          = games_played
        self.creator        = creator

    @classmethod
    def from_json(cls, j):
        name                = j["name"]
        rating              = Rating.from_json(j["rating"])
        delta_rating        = j["delta_rating"]
        inactive            = j["inactive"]
        creator             = j["creator"]
        games               = j["games"]
        return cls(name, rating, delta_rating, inactive, games, creator)

    def update_rating(self, rating: Rating, was_active: bool, number_of_games = 0):
        self.delta_rating   = rating.get_display_rating() - self.get_rating().get_display_rating()
        self.rating         = rating
        self.games          += number_of_games
        if was_active:      self.inactive = 0
        else:               self.inactive += 1

    def get_rating(self):   return self.rating
    def get_inactive(self): return self.inactive

    def to_json(self):
        return {"name": self.name, 
                "rating": self.rating.to_json(), 
                "delta_rating": self.delta_rating, 
                "games": self.games, 
                "inactive": self.inactive, 
                "creator": self.creator }

    def __repr__(self):     return f"{self.name} ({self.rating}) [{round(self.delta_rating)}]"
    def __str__(self):      return self.name
