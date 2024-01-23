import random
import Data
import discord
import clr
import os
import asyncio
import twich
from discord.colour import Color
from discord.embeds import Embed
from discord.message import Message
from discord.ext import tasks
from discord.ext import commands
from discord import app_commands
from discord import TextChannel
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import StreamOnlineEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope

curDir = os.path.dirname(os.path.abspath(__file__))
curDirs = os.path.split(curDir)
ldcDir = curDirs[len(curDirs) - 2]

clr.AddReference(r"System")
clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\obj\Debug\LDC.ClassesLibrary.dll"))
clr.AddReference(os.path.join(ldcDir, r"LDC.ClassesLibrary\packages\EntityFramework.6.4.4\lib\net45\EntityFramework.dll"))

from LDC.ClassesLibrary import *
from System.Collections.Generic import *
from System import *


@tasks.loop(seconds=5)
async def on_stream_online():
    general = bot.get_channel(int(Data.TwitcGeneralChannelID))
    stream = twich.checkIfLive(Data.TwitchUsersLoggins)
    message = t_controler.get_message()
    if(stream != "OFFLINE" and general != None):
        print("[LDC] Stream online!")
        if(message == None):
            await t_controler.send_message(general=general, stream=stream)
        else:
            await t_controler.edit_message(stream=stream)

    if(stream == "OFFLINE" and message != None):
        print("[LDC] Stream end!")
        await t_controler.drop_message(general)

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "?", intents = intents)

    async def setup_hook(self):
        await self.tree.sync()
        on_stream_online.start()
        print(f"Synced slash commands for {self.user}.")
        
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)
    
class SignFlags(commands.FlagConverter):
    bunti_1: int = 0
    ayur_2: int = 0
    dodor_3: int = 0
    takhar_4: int = 0    


class TwitchNotificationController():
    message:Message = None

    def get_message(self):
        return self.message

    async def send_message(self, general, stream):
        self.message = await general.send(f"{Data.TwitchStreamUpMessage} \n :game_die: Играем в: **{stream.game}** \n :busts_in_silhouette: Зрителей: **{stream.viewer_count}**")
    
    async def edit_message(self, stream):
        await self.message.edit(content=f"{Data.TwitchStreamUpMessage} \n :game_die: Играем в: **{stream.game}** \n :busts_in_silhouette: Зрителей: **{stream.viewer_count}**")


    async def drop_message(self, general):
        if(self.message != None):
            await self.message.delete()
            self.message = None
            await general.send(content=f"Трансляция завершилась, спасибо всем за участие :purple_heart: ")


t_controler = TwitchNotificationController()
bot = Bot() 

def get_sign_embed(bunti_1, ayur_2, dodor_3, takhar_4) -> Embed:
    #Второй параметр поставить в True, если первый запуск
    lib = EnoaLibrary(None, False)
    color = discord.Color
    signsResponce = lib.GetSign(bunti_1, ayur_2, dodor_3, takhar_4)
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
        embed = Embed(title="Ошибка", color=color.red(), description=f"Не было обнаружено знамение по переданным данным {bunti_1}, {ayur_2}, {dodor_3}, {takhar_4}")   
    return embed

@bot.hybrid_command(name = "rsign", with_app_command = True, description = "Random Sign")
async def get_rsign(ctx: commands.Context):

    lib = EnoaLibrary(None, False)
    allSignsResponce = lib.GetSigns()
    signs = allSignsResponce.Result
    rnum = random.randint(0, signs.Count - 1)
    rsign = signs[rnum]

    embed = get_sign_embed(rsign.Bunti, rsign.Ayur, rsign.Dodor, rsign.Takhar)
    await ctx.defer(ephemeral = False)
    await ctx.send(embed=embed) 

@bot.hybrid_command(name = "sign", with_app_command = True, description = "Sign")
async def get_sign(ctx: commands.Context, flags: SignFlags):
    embed = get_sign_embed(flags.bunti_1, flags.ayur_2, flags.dodor_3, flags.takhar_4)
    await ctx.defer(ephemeral = False)
    await ctx.send(embed=embed) 

bot.run(Data.TokenDiscord)
