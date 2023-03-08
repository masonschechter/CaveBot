import sqlite3

#Crontab runs this every day at 4:20 pm CST

con = sqlite3.connect('/home/mason/python/home-projects/CaveBot/CaveBot.db')
db = con.cursor()

db.execute('UPDATE High_Rollers SET Balance = Balance + 420') ##blaze it
con.commit()