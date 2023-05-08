import Player

class Score():
    def __init__(self, wins1, wins2):
        self.wins1 = wins1
        self.wins2 = wins2

    def get_winrate(self, player = 1):  
        if player == 2:     return self.wins2 / (self.wins1 + self.wins2)
        return self.wins1 / (self.wins1 + self.wins2)

    def to_json(self):      return (self.wins1, self.wins2)
    def __str__(self):      return f"{self.wins1} - {self.wins2}"


class Result():
    def __init__(self, submitter, time, channel, player1, player2, score):
        self.submitter  = submitter
        self.time       = time
        self.channel    = channel
        self.player1    = player1
        self.player2    = player2
        self.score      = score

    @classmethod
    def from_json(cls, j):
        return cls(j["Metadata"]["Submitter"], 
                   j["Metadata"]["Time"], 
                   j["Metadata"]["Channel"], 
                   j["Payload"]["Player1"], 
                   j["Payload"]["Player2"], 
                   Score(*j["Payload"]["Score"]))

    def get_metadata(self):
        return (self.submitter, self.time, self.channel)
    def get_result(self): 
        return (self.player1, self.player2, self.score)
    def get_submitter(self):
        return self.submitter

    def contains(self, player):
        if self.player1 == player:      return 1 
        elif self.player2 == player:    return 2
        return 0

    def equals(self, other):
        if not self.submitter == other.submitter: return False
        if (self.player1 == other.player1 and self.player2 == other.player2 and self.score.wins1 == other.score.wins1 and self.score.wins2 == other.score.wins2): return True
        if (self.player1 == other.player2 and self.player2 == other.player1 and self.score.wins1 == other.score.wins2 and self.score.wins2 == other.score.wins1): return True
        return False

    def glickofy(self, player):
        if not self.contains(player): raise KeyError(f"Player {player} was not part of the match {self}.")
        if self.player1 == player:   return (self.player2.get_rating().rating, self.player2.get_rating().rd,  self.score.get_winrate(1))
        if self.player2 == player:   return (self.player1.get_rating().rating, self.player1.get_rating().rd,  self.score.get_winrate(2))

    def to_json(self):  return {"Metadata": {"Submitter": self.submitter, 
                                             "Time": self.time, 
                                             "Channel": self.channel}, 
                                "Payload": {"Player1": self.player1.name, 
                                            "Player2": self.player2.name, 
                                            "Score": self.score.to_json()}}
    def __str__(self):  return f"{self.player1}  {self.score}  {self.player2}"
    def __repr__(self): return f"Submitted score by {self.submitter} at time {self.time} : {self.player1}  --- {self.score} --- {self.player2}"