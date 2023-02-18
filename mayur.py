import sqlite3
conn = sqlite3.connect("mj.db")
def lol():
    ct = ("CREATE TABLE IF NOT EXISTS Contacts (sno integer PRIMARY KEY,	name text,email varchar, phone_num int, msg text, date varchar);")
    c = conn.cursor()
    c.execute(ct)
lol()

def lmao():
    ct = ("CREATE TABLE IF NOT EXISTS Posts (sno integer PRIMARY KEY,	title text,tagline text, slug int, content text, date text);")
    c = conn.cursor()
    c.execute(ct)
lmao()


conn.commit()
conn.close()
