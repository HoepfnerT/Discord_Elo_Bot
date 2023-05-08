import json, datetime

class Verifier:
    def __init__(self, member_dict = {i: [] for i in range(1,6)}, channel_dict = {i: [] for i in range(1,6)}, role_dict = {i: [] for i in range(1,6)}, filepath = ""):
        self.member_dict    = member_dict
        self.channel_dict   = channel_dict
        self.role_dict      = role_dict
        self.filepath       = filepath

    @classmethod
    def from_file(cls, file, filepath = ""): 
        with open(filepath + file, "r") as f:
            js = json.load(f)
            return cls(js["member"], js["channel"], js["roles"], filepath = filepath)

    def verify_ctx(self, ctx):
        with open(self.filepath + ".log", "a+") as f:
            if ctx.message == None: return -1
            log_msg                                  = f"{datetime.datetime.now()} \n" 
            log_msg                                 += f" ----- User -- {ctx.message.author.id} - {ctx.message.author.name}\n"
            if ctx.message.guild != None:   log_msg += f" --- Server -- {ctx.message.guild.id} - {ctx.message.guild.name}\n"
            if ctx.message.channel != None: log_msg += f" -- Channel -- {ctx.message.channel.id} - {ctx.message.channel.name}\n"
            if ctx.message.content != None: log_msg += f" -- Message -- {ctx.message.id} - {ctx.message.content}\n"
            print(log_msg)
            f.write(log_msg)
        for i in range(5,0,-1):
            if ctx.message.author   != None and ctx.message.author.id  in self.member_dict[str(i)]:  return i
            if ctx.message.channel  != None and ctx.message.channel.id in self.channel_dict[str(i)]: return i
            if ctx.message.author   != None:
                for role in ctx.message.author.roles:
                    if role.id in self.role_dict[str(i)]: return i
        return 0