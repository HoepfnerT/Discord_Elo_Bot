import json, os
from dotenv import load_dotenv
from Leaderboard_Handler import Leaderboard_Handler
from Leaderboard import Leaderboard
from Discord_Interface import Discord_Interface
from Verifier import Verifier
import glob

if __name__ == "__main__":
    ############################### LOAD ENVIRONMENTAL VARIABLES FROM .env AND SETUP THE BOT ###############################
    load_dotenv()                                                                       # load from .env                 ###
    PATH = os.getenv("LOCATION")                                                        # Path to main folder            ###
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")                                  # Bot Token for the Discord Bot  ###
    ADMIN_CHANNEL = int(os.getenv("ADMIN_DISCORD_CHANNEL"))                             # Channel on my privat Discord   ###
    ########################################################################################################################

    try:
        list_of_files = glob.glob(PATH + "out/*_save.json") 
        latest_file = max(list_of_files, key=os.path.getctime)
        print(f"Loading leaderboard from {latest_file}.")
        discord_interface = Discord_Interface(DISCORD_BOT_TOKEN, ADMIN_CHANNEL,
                                              Leaderboard_Handler.from_file(latest_file,  filepath=PATH + "out/"),
                                              Verifier.from_file(file = ".auth", filepath = PATH))
    except Exception as e:
        LEADERBOARD = Leaderboard()
        discord_interface = Discord_Interface(DISCORD_BOT_TOKEN, ADMIN_CHANNEL, 
                                              Leaderboard_Handler(LEADERBOARD, filepath=PATH + "out/"),
                                              Verifier.from_file(file = ".auth", filepath = PATH))

    discord_interface.start()

    
