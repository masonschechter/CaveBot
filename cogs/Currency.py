import discord
import asyncio
import random
from discord.ext import commands
from numpy.random import choice as nprc
import const
import sqlite3
from beautifultable import BeautifulTable
import re

con = sqlite3.connect('CaveBot.db')


class Currency(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def nugs(self, ctx, user: discord.Member = None):

		if not user:
			user = ctx.author

		balance = self.getBalance(user)

		await ctx.send(f"{user.mention} has {balance} nugs")

	@commands.command()
	async def gamble(self, ctx, bet):

		balance = self.getBalance(ctx.author)
		allIN = False

		if bet.lower() == 'all':
			bet = balance
			allIN = True
		elif re.match(r'\d+%', bet): ## its a %
			bet = int(int(re.match(r'\d+',bet).group(0))/100*balance)
			if bet == balance:
				allIN = True
		else:
			bet = int(bet)

		db = con.cursor()
		if bet <= balance:
			if nprc([0,1]):
				newBalance = balance + bet
				db.execute("UPDATE High_Rollers SET Balance = ? WHERE Discord_ID = ?", (newBalance, ctx.author.id))
				con.commit()
				if allIN:
					await ctx.send(f"LETS GOOOOOOOOOO! {ctx.author.mention} chucked his bank and WON!\nNew balance: {newBalance} nugs.")
				else:
					await ctx.send(f"{ctx.author.mention} WON {bet} nugs POG!\nNew balance: {newBalance} nugs")
			else:
				newBalance = balance - bet
				db.execute("UPDATE High_Rollers SET Balance = ? WHERE Discord_ID = ?", (newBalance, ctx.author.id))
				con.commit()
				if allIN:
					await ctx.send(f"CYA HICK! {ctx.author.mention} chucked his bank and LOST!\nNew Balance: {newBalance} nugs")
				else:
					await ctx.send(f"Yikes, {ctx.author.mention} LOST {bet} nugs!\nNew balance: {newBalance} nugs")
		else:
			await ctx.send(f"Yerrr poor, {ctx.author.mention}.\nYou can't gamble {bet}. You only have {balance} nugs")
	
	@commands.command()
	@commands.has_role('Enforcers')
	async def give(self, ctx, amount: int, user: discord.Member = None):

		if not user:
			user = ctx.author

		db = con.cursor()
		balance = self.getBalance(user)
		newBalance = balance + amount
		db.execute("UPDATE High_Rollers SET Balance = ? WHERE Discord_ID = ?", (newBalance, user.id))
		con.commit()

		await ctx.send(f"{user.mention} now has {newBalance} nugs!")

	@commands.command()
	async def stake(self, ctx, amount:int, user: discord.Member):

		balance1 = self.getBalance(ctx.author)
		balance2 = self.getBalance(user)

		if balance1 < amount:
			await ctx.send(f"Oof, {ctx.author.mention}.\nYou can't stake for {amount}; you only have {balance1} nugs")
			return

		if balance2 < amount:
			await ctx.send(f"Sorry, {ctx.author.mention}, {user.mention} is a poor boi.\nYou can't stake for {amount}; they only have {balance2} nugs")
			return

		def player2Check(message):
			return message.author == user and message.content == 'esketit'

		await ctx.send(f"{ctx.author.mention} wants to stake {user.mention} for {amount}.\n{user.mention}, you have 5 minutes to type 'esketit' to accept.")
		
		try:
			await self.bot.wait_for('message', timeout=300, check=player2Check)
		except asyncio.TimeoutError:
			await ctx.send(f"RIP, {user.mention} didn't respond in time.")
		else:
			db = con.cursor()
			if nprc([0,1]): ##player 1 (offense) wins
				newBalance1 = balance1 + amount
				newBalance2 = balance2 - amount
				db.execute("UPDATE High_Rollers SET Balance = ?, Wins = Wins + 1 WHERE Discord_ID = ?", (newBalance1, ctx.author.id))
				db.execute("UPDATE High_Rollers SET Balance = ?, Losses = Losses + 1 WHERE Discord_ID = ?", (newBalance2, user.id))
				con.commit()
				await ctx.send(f"""{ctx.author.mention} beat {user.mention} for {amount} nugs!\n\n{ctx.author.mention}'s new balance: {newBalance1} nugs.\n{user.mention}'s new balance: {newBalance2} nugs.""")
			else: ## player 2 (defence) wins
				newBalance2 = balance2 + amount
				newBalance1 = balance1 - amount
				db.execute("UPDATE High_Rollers SET Balance = ?, Wins = Wins + 1 WHERE Discord_ID = ?", (newBalance2, user.id))
				db.execute("UPDATE High_Rollers SET Balance = ?, Losses = Losses + 1 WHERE Discord_ID = ?", (newBalance1, ctx.author.id))
				con.commit()
				await ctx.send(f"""{user.mention} beat {ctx.author.mention} for {amount} nugs!\n\n{user.mention}'s new balance: {newBalance2} nugs.\n{ctx.author.mention}'s new balance: {newBalance1} nugs.""")

	@commands.command()
	async def leaderboard(self, ctx):
		db = con.cursor()
		table = BeautifulTable()
		table.column_headers = ["Rank", "Name", "Nugs", "Wins", "Losses", "W/L Ratio"]
		rank = 1
		top10 = db.execute("SELECT * FROM High_Rollers ORDER BY Balance DESC LIMIT 10 ")
		for row in top10:
			user = await self.bot.fetch_user(row[0])
			wins = row[2]
			losses = row[3]
			winRatio = round(wins/(wins+losses), 3) if losses else 'N/A'
			userData = [rank, user.name, row[1], wins, losses, winRatio]
			table.append_row(userData)
			rank += 1
		await ctx.send(f"```{table}```")

	def getBalance(self, user: discord.Member):

		db = con.cursor()
		result = db.execute("SELECT Balance FROM High_Rollers WHERE Discord_ID = ?", (user.id,)).fetchone() ##if the user already exists

		if not result: ## if they don't
			db.execute("INSERT INTO High_Rollers (Discord_ID, Balance, Wins, Losses) VALUES (?, ?, ?, ?)", (user.id, 420, 0, 0))
			con.commit()
			balance = 420
			return balance

		return result[0]


def setup(bot):
	bot.add_cog(Currency(bot))