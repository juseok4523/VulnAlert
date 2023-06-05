import discord
from discord.ext import commands
import os

bot_token = os.environ['BOT_TOKEN']
prefix = '!'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

