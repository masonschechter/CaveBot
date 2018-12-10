import discord
import asyncio
import random
from discord.ext import commands
import const

OwnerID = const.OWNER_ID
BotID = const.BOT_ID
Token = const.TOKEN
bot = commands.Bot(command_prefix=const.COMMAND_PREFIX)

@bot.event
async def on_ready():
	print("====================")
	print("Logged in as")
	print(bot.user.name)
	print(bot.user.id)
	print("====================")
    
@bot.command()
async def hello(ctx):
    await ctx.send('Wussup, my dude')

@bot.command()
async def Buloz(ctx):
	await ctx.send('Buloz is a gentleman and a scholar')


@bot.command()
async def mock(ctx, *mocked):
	name = " ".join(mocked)
	message = await ctx.channel.history().get(author__name=name)
	mocking = list(message.content)
	mockery = []
	for i in range(0, len(mocking)):
		if i % 2 == 1:
			mockery.append(str.upper(mocking[i]))
		else:
			mockery.append(str.lower(mocking[i]))
	await ctx.send("'" + ''.join(mockery) + "' " + "-- " + message.author.mention)



@bot.command()
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


	emoji_role = {
		'Fortnite':'Fortnite', 'CSGO':'CSGO', 'WoW':'WoW', 'PUBG':'PUBG',
		'OSRS':'OSRS', 'Hots':'Heroes of the Storm', 'Hearthstone':'Hearthstone',
		'League':'League of Legends', 'Overwatch':'Overwatch', 'Dota':'Dota'}

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

	emoji_role = {
		'Fortnite':'Fortnite', 'CSGO':'CSGO', 'WoW':'WoW', 'PUBG':'PUBG',
		'OSRS':'OSRS', 'Hots':'Heroes of the Storm', 'Hearthstone':'Hearthstone',
		'League':'League of Legends', 'Overwatch':'Overwatch', 'Dota':'Dota'}

	if emoji.name in emoji_role:
		role = discord.utils.get(guild.roles, name=emoji_role[emoji.name])
		if role in member.roles:
			await member.remove_roles(role)































bot.run(Token, bot=True)