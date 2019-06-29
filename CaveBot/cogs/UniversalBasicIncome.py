import sqlite3

con = sqlite3.connect('/home/mason/python/home-projects/CaveBot/CaveBot.db')
db = con.cursor()

db.execute('UPDATE High_Rollers SET Balance = Balance + 420') ##blaze it
con.commit()