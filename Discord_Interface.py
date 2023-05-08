from Leaderboard_Handler import Leaderboard_Handler
from Discord_Bot_Glicko import Discord_Bot_Glicko
from Verifier import Verifier

class Discord_Interface():
    def __init__(self, discord_bot_token, admin_channel, leaderboard_handler: Leaderboard_Handler, verifier: Verifier):
        self.leaderboard_handler    = leaderboard_handler
        self.discord_bot_token      = discord_bot_token
        self.admin_channel          = admin_channel
        self.verifier               = verifier

    def start(self):
        self.discord_bot = Discord_Bot_Glicko(command_prefix='!', admin_channel = self.admin_channel, leaderboard_handler = self.leaderboard_handler, verifier = self.verifier)
        self.discord_bot.run(self.discord_bot_token)