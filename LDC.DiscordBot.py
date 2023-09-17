import discord
import clr
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from decouple import config
from discord import app_commands

clr.AddReference(r"D:\Programs\LDC\LDC.EnoaLibrary\bin\Debug\net6.0\LDC.EnoaLibrary.dll")
clr.AddReference(r"D:\Programs\LDC\LDC.DiscordBot\libs\Microsoft.EntityFrameworkCore.dll")

from Microsoft.EntityFrameworkCore import DbContext
from LDC.EnoaLibrary import EnoaLibrary
from LDC.EnoaLibrary.Classes import SignContextInitializer


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
    cont = SignContextInitializer()
    lib = EnoaLibrary()
    #lib = CDLL(r"D:\Programs\LDC\LDC.EnoaLibrary\bin\Debug\net6.0\LDC.EnoaLibrary.dll") 
    #int_bunti = c_int(flags.bunti_1)
    #int_ayur = c_int(flags.ayur_2)
    #int_dodor = c_int(flags.dodor_3)
    #int_takhar = c_int(flags.takhar_4)
    #resp = lib.EnoaLibrary()
    #GetSign(int_bunti, int_ayur, int_dodor, int_takhar)

    color = discord.Color
    embed = Embed(title="Знамение", color=color.blue(), description="Описание знамения")
    await ctx.defer(ephemeral = False)
    await ctx.send(embed=embed)

bot.run(token)