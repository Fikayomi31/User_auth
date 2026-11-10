import sqlite3

con = sqlite3.connect("test.db")
print(con.execute("select name from sqlite_master where type='table'").fetchall())