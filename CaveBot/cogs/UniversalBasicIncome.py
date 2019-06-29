import sqlite3

con = sqlite3.connect('../CaveBot.db')
db = con.cursor()

db.execute('UPDATE High_Rollers SET Balance = Balance + 420')
db.commit()