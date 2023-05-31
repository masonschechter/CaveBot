import discord
import asyncio
import random
from discord.ext import commands
import const
import sqlite3
from numpy.random import choice as nprc
from cogs.Currency import Currency

OwnerID = const.OWNER_ID
BotID = const.BOT_ID
Token = const.TOKEN
intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix=const.COMMAND_PREFIX)

emoji_role = {
        'Fortnite':'Fortnite', 'CSGO':'CSGO', 'WoW':'WoW', 'PUBG':'PUBG',
        'OSRS':'OSRS', 'Hots':'Heroes of the Storm', 'Hearthstone':'Hearthstone',
        'League':'League of Legends', 'Overwatch':'Overwatch', 'Dota':'Dota', 'Apex':'Apex', 
        'Mordhau':'Mordhau', 'Underlords':'Underlords','Starcraft2':'Starcraft2', 
        'Minecraft':'Minecraft', 'Valorant':'Valorant', 'Spellbreak':'Spellbreak', 
        'DayZ':'DayZ', 'AmongUs':'Among Us', 'SSBM':'SSBM', 'Tarkov':'Tarkov', 
        'Battlefront2':'Battlefront 2', 'DeepRockGalactic':'Deep Rock Galactic'}

# bot.load_extension('cogs.Currency')

def is_owner(ctx):
    return ctx.author.id == OwnerID

def is_botTest(ctx):
    return ctx.channel.id == 390306184751480835

@bot.event
async def on_ready():
    print("====================")
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("====================")

    await bot.add_cog(Currency(bot))
    
@bot.command()
async def hello(ctx):
    await ctx.send('Wussup, my dude')

@bot.command()
async def Buloz(ctx):
    await ctx.send('Buloz is a gentleman and a scholar')


@bot.command()
async def mock(ctx, mocked: discord.Member): ## will accept name, nickname, mention, userID, and name#discrim
    messages = ctx.channel.history(limit=100)
    message_ID = 0
    async for m in messages:
        if not message_ID:
            if not m.author.name == mocked.name:
                pass
            else:
                message_ID = m.id
    if not message_ID:
        await ctx.send("I couldn't find a recent message by that user in this channel")
    else:
        message = await ctx.channel.fetch_message(message_ID)
        mocking = list(message.clean_content)
        mockery = []
        for i in range(0, len(mocking)):
            if i % 2 == 1:
                mockery.append(str.upper(mocking[i]))
            else:
                mockery.append(str.lower(mocking[i]))
        await ctx.send(f"{''.join(mockery)}")


@bot.command(name='8ball')
async def eightball(ctx, *, yes_or_no_question):
    responses = ['It is decidedly so', 'Without a doubt',
                        'Yes, definitely', 'You may rely on it', 'As I see it, yes', 'Signs point to yes',
                        'My crystal ball ain\'t so crystal clear', 'Concentrate and ask again',
                        'Don\'t count on it', 'That\'s gunna be a no from me, dog', 'My sources say no',
                        'Outlook not so good', 'Very doubtful', 
                        'Yes, No, Maybe...I don\'t know, could you repeat the question?', 'You wish, kid', 
                        'How am I supposed to know? I\'m just a bot', 'Is the Pope Catholic?', 'Damn straight']
    await ctx.send(random.choice(responses))


@bot.event
async def on_raw_reaction_add(payload):
    role_channel = bot.get_channel(const.ROLE_CHANNEL)
    channel = bot.get_channel(payload.channel_id)
    if not role_channel == channel:
        return

    emoji = bot.get_emoji(payload.emoji.id)
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if emoji.name in emoji_role:
        role = discord.utils.get(guild.roles, name=emoji_role[emoji.name])
        if role not in member.roles:
            await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    role_channel = bot.get_channel(const.ROLE_CHANNEL)
    channel = bot.get_channel(payload.channel_id)
    if not role_channel == channel:
        return

    emoji = bot.get_emoji(payload.emoji.id)
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if emoji.name in emoji_role:
        role = discord.utils.get(guild.roles, name=emoji_role[emoji.name])
        if role in member.roles:
            await member.remove_roles(role)

@bot.event
async def on_command_error(ctx,error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Uh oh! My owner didn't teach me that trick :(\nMake sure you're typing the command correctly and try again.")
    elif isinstance(error, commands.MissingRole):
        await ctx.send(f"Sorry bud, you don't have the permissions/role to use this command.")
    else:
        await ctx.send(f"Beep Boop! I'm a broken bot :)")

bot.run(Token)