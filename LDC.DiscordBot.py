import discord
import clr
import sys
import os
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from decouple import config
from discord import app_commands


curDir = os.path.dirname(os.path.abspath(__file__))
curDirs = os.path.split(curDir)
ldcDir = curDirs[len(curDirs) - 2]

clr.AddReference(r"System")
clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\obj\Debug\LDC.ClassesLibrary.dll"))
clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\EntityFramework.6.4.4\lib\net45\EntityFramework.dll"))
clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\EntityFramework.6.4.4\lib\net45\EntityFramework.SqlServer.dll"))

from LDC.ClassesLibrary import *
from System.Collections.Generic import *


token = config('token',default='')


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

bot = Bot()

@bot.hybrid_command(name = "sign", with_app_command = True, description = "Sign")
async def test(ctx: commands.Context, flags: SignFlags):
    #Второй параметр поставить в True, если первый запуск
    lib = EnoaLibrary(None, False)
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

bot.run(token)