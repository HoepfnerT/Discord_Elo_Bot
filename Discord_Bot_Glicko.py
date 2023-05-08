import discord
from discord.ext import commands, tasks
from Leaderboard_Handler import Leaderboard_Handler
from Costum_Exceptions import DiscordInputError
from Verifier import Verifier
import re

_REACT_CONFIRM = "\u2705"
_REACT_DENY = "\u26D4"

_ADMIN = 5
_MODERATOR = 3
_VERIFIED = 1
_USER = 0

class Discord_Bot_Glicko(commands.Bot):
    async def send_leaderboard(self, ctx, predict = False, min_games = 10, inactive_threshhold = 3):
        if predict:             msg = str(self.leaderboard_handler.get_prediction(min_games=min_games, inactive_threshhold=inactive_threshhold))
        else:                   msg = str(self.leaderboard_handler.get_ranking(min_games=min_games, inactive_threshhold=inactive_threshhold))
        if len(msg) > 0:        await ctx.send(msg)
        else:                   await ctx.send("Leaderboard not found.")
    
    async def send_pending(self, ctx):
        msg = str(self.leaderboard_handler.get_pending())
        if len(msg) > 0:        await ctx.send(msg)
        else:                   await ctx.send("Leaderboard not found.")
    
    @tasks.loop(hours=24)
    async def save_to_file(self):
        print("Saving ...")
        self.leaderboard_handler.to_file()
        print("Done.")


    def __init__(self, admin_channel, command_prefix='!', leaderboard_handler = Leaderboard_Handler(), verifier = Verifier()):
        intents                         = discord.Intents.default()
        intents.members                 = True
        intents.messages                = True
        super().__init__(command_prefix = command_prefix, intents=intents)
        self.leaderboard_handler        = leaderboard_handler
        self.verifier                   = verifier
        self.admin_channel              = admin_channel

        

        @self.event
        async def on_ready():
            print("Discord Bot is running...")
            self.save_to_file.start()
            #ch = self.get_channel(self.admin_channel)
            #await ch.send(self.all_commands.keys())

        @self.command()
        async def ping(ctx):
            #if self.verifier.verify_ctx(ctx) < _VERIFIED:
            await ctx.send("Hello.")
            return


        async def regularise_name(name: str):
            name = ''.join(c for c in name if c.isalnum())
            if not name: raise Exception("Name after regularising is empty.")
            return name

        async def get_result(ctx):
            try:    
                msg = re.sub(r"![^ ]* (.*)", r"\1", ctx.message.content)
                cmds = msg.split()
                guilds, scores = [a for a in cmds if not a.isdigit()], [int(a) for a in cmds if a.isdigit()]
                if len(guilds) != 2 or len(scores) != 2: raise DiscordInputError
                player1, player2, score1, score2 = *guilds, *scores
                player1 = await regularise_name(player1)
                player2 = await regularise_name(player2)
                return (player1, player2, score1, score2)
            except Exception as e: 
                raise e

        @self.command(aliases = ["new","addplayer","newplayer","addguild", "newguild"])
        async def add(ctx):
            if self.verifier.verify_ctx(ctx) < _VERIFIED: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            name = re.sub(r"![^ ]* (.*)", r"\1", ctx.message.content)
            try:    name = await regularise_name(name)
            except Exception as e:
                print(e)
                await ctx.send("Could not add this player. Use !new PlayerName. The Player name must consist of characters and numbers only with at least one character.")
            if name.isdigit(): 
                await ctx.send("Name cannot consist only of numbers.")
                await ctx.message.add_reaction(_REACT_DENY)
                return
            self.leaderboard_handler.add_player(name, creator = ctx.message.author.id)
            self.leaderboard_handler.to_file()
            await ctx.message.add_reaction(_REACT_CONFIRM)
            
        @self.command(aliases = ["submit", "gvg", "enter", "score", "result"])
        async def report(ctx):
            if self.verifier.verify_ctx(ctx) < _VERIFIED: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            try:    
                player1, player2, score1, score2 = await get_result(ctx)
                print(f"{player1} {player2} {score1} {score2}")
            except Exception as e:
                print(e)
                await ctx.send("I couldn't parse that, sorry! Use \"!report Guild1 Guild2 Score1 Score2\"")
                return
            if not self.leaderboard_handler.is_player(player1) and not self.leaderboard_handler.is_player(player2):
                await ctx.send(f"The guilds [{player1}] and [{player2}] is not yet known to me. Please check the spelling or add them.")
                return
            if not self.leaderboard_handler.is_player(player1):
                await ctx.send(f"The guilds [{player1}] is not yet known to me. Please check the spelling or add them.")
                return
            if not self.leaderboard_handler.is_player(player2):
                await ctx.send(f"The guilds [{player2}] is not yet known to me. Please check the spelling or add them.")
                return
            if score1 > score2:     await ctx.send(f"[{player1}] won vs. [{player2}] with a score of {score1} : {score2}.")
            elif score1 < score2:   await ctx.send(f"[{player2}] won vs. [{player1}] with a score of {score2} : {score1}.")
            elif score1 == score2:  await ctx.send(f"[{player1}] drew vs. [{player2}] with a score of {score1} each.")
            self.leaderboard_handler.add_result(player1, player2, score1, score2, ctx.message.author.id, str(ctx.message.created_at), ctx.message.channel.id)
            self.leaderboard_handler.to_file()
            await ctx.message.add_reaction(_REACT_CONFIRM)

        @self.command(aliases=["delete", "undo"])
        async def remove(ctx):
            if self.verifier.verify_ctx(ctx) < _VERIFIED: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            try:    
                player1, player2, score1, score2 = await get_result(ctx)
            except: 
                await ctx.send("I couldn't parse that, sorry! Use \"!remove Guild1 Guild2 Score1 Score2\"")
                return

            if self.leaderboard_handler.remove_result(player1, player2, score1, score2, ctx.message.author.id, str(ctx.message.created_at), ctx.message.channel.id):
                self.leaderboard_handler.to_file()
                await ctx.message.add_reaction(_REACT_CONFIRM)
            else:
                await ctx.message.add_reaction(_REACT_DENY)

        @self.command(aliases=[])
        async def clear_results(ctx):
            if self.verifier.verify_ctx(ctx) < _VERIFIED: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            self.leaderboard_handler.clear_results()
            self.leaderboard_handler.to_file()
            await ctx.message.add_reaction(_REACT_CONFIRM)

        @self.command()
        async def save(ctx):
            if self.verifier.verify_ctx(ctx) < _ADMIN: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            self.leaderboard_handler.to_file()
            await ctx.message.add_reaction(_REACT_CONFIRM)

        @self.command(aliases = [])
        async def commit(ctx):
            if self.verifier.verify_ctx(ctx) < _ADMIN: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            self.leaderboard_handler.resolve_results()
            await ctx.message.add_reaction(_REACT_CONFIRM)
            
        @self.command(aliases = ["ranking"])
        async def rankings(ctx):
            if self.verifier.verify_ctx(ctx) < _USER: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            await self.send_leaderboard(ctx)
            await ctx.message.add_reaction(_REACT_CONFIRM)

        @self.command(aliases = [])
        async def ranking_details(ctx):
            if self.verifier.verify_ctx(ctx) < _MODERATOR: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            await self.send_leaderboard(ctx, min_games = 0, inactive_threshhold = 999999)
            await ctx.message.add_reaction(_REACT_CONFIRM)

        @self.command(aliases = [])
        async def live(ctx):
            if self.verifier.verify_ctx(ctx) < _USER: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            await self.send_leaderboard(ctx, predict = True)
            await ctx.message.add_reaction(_REACT_CONFIRM)

        @self.command(aliases = [])
        async def live_details(ctx):
            if self.verifier.verify_ctx(ctx) < _MODERATOR: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            await self.send_leaderboard(ctx, min_games = 0, inactive_threshhold = 999999, predict = True)
            await ctx.message.add_reaction(_REACT_CONFIRM)

        @self.command(aliases = ["results", "recent"])
        async def pending(ctx):
            if self.verifier.verify_ctx(ctx) < _USER: 
                await ctx.message.add_reaction(_REACT_DENY)
                return
            await self.send_pending(ctx)
            await ctx.message.add_reaction(_REACT_CONFIRM)