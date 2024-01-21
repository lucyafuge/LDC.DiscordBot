import discord
import clr
import os
import Data
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from discord import app_commands

curDir = os.path.dirname(os.path.abspath(__file__))
curDirs = os.path.split(curDir)
ldcDir = curDirs[len(curDirs) - 2]

clr.AddReference(r"System")
clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\obj\Debug\LDC.ClassesLibrary.dll"))
clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\EntityFramework.6.4.4\lib\net45\EntityFramework.dll"))

from LDC.ClassesLibrary import *
from System.Collections.Generic import *
from System import *

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "?", intents = intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}.")
        
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)

class SignFlags(commands.FlagConverter):
    bunti_1: int = 0
    ayur_2: int = 0
    dodor_3: int = 0
    takhar_4: int = 0

def InitDiscordBot():
    bot = Bot()

    @bot.hybrid_command(name = "sign", with_app_command = True, description = "Sign")
    async def get_sign(ctx: commands.Context, flags: SignFlags):
        #Второй параметр поставить в True, если первый запуск
        lib = EnoaLibrary(None, True)
        color = discord.Color
        signsResponce = lib.GetSign(flags.bunti_1, flags.ayur_2, flags.dodor_3, flags.takhar_4)
        sign = signsResponce.Result
        if(sign != None):
            desc = f"\
            Кости: ({sign.Bunti}, {sign.Ayur}, {sign.Dodor}, {sign.Takhar}) \n\n \
            Сложность: {sign.Difficult} \n\n \
            {sign.Description } \n\n \
            Эффект: {sign.Effect} \n\n \
            Успех: {sign.Success} \n\n \
            Провал: {sign.Failure} \n\n \
            "
            embed = Embed(title=sign.Name, color=color.blue(), description=desc)
        else:
            embed = Embed(title="Ошибка", color=color.red(), description="Не было обнаружено знамение по переданным данным")    

        await ctx.defer(ephemeral = False)
        await ctx.send(embed=embed) 
        bot.run(Data.TokenDiscord)
    return bot

        



#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\Microsoft.Extensions.Logging.Abstractions.8.0.0\lib\netstandard2.0\Microsoft.Extensions.Logging.Abstractions.dll"))
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\Newtonsoft.Json.13.0.3\lib\netstandard2.0\Newtonsoft.Json.dll"))
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\TwitchLib.Api.Core.3.9.0\lib\netstandard2.0\TwitchLib.Api.Core.dll"))
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\TwitchLib.Api.Core.Enums.3.9.0\lib\netstandard2.0\TwitchLib.Api.Core.Enums.dll"))
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\TwitchLib.Api.Core.Interfaces.3.9.0\lib\netstandard2.0\TwitchLib.Api.Core.Interfaces.dll"))
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\TwitchLib.Api.Helix.3.9.0\lib\netstandard2.0\TwitchLib.Api.Helix.dll"))
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\TwitchLib.Api.Helix.Models.3.9.0\lib\netstandard2.0\TwitchLib.Api.Helix.Models.dll"))
#
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\TwitchLib.Api.3.9.0\lib\netstandard2.0\TwitchLib.Api.dll"))
#clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\TwitchLib.Communication.2.0.1\lib\netstandard2.0\TwitchLib.Communication.dll"))

#from TwitchLib.Api import Services
#twich_lib.LiveStreamMonitor.OnStreamOnline += alert_stream_message
#dOnStreamOnline = EventHandler[Services.Events.LiveStreamMonitor.OnStreamOnlineArgs](alert_stream_message)
#twich_lib.LiveStreamMonitor.OnStreamOnline("asd", "asdsd")
#twich_lib.LiveStreamMonitor.Start()