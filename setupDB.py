import sqlite3

conn = sqlite3.connect("dfs.db")
c = conn.cursor()

c.execute('''CREATE TABLE CONTESTS
             ([Name] text, [Prize Pool] float, [Buy In] float, [Top Prize] integer,
                [Max Entries] integer, [Entries] integer, [Cash Line] float,
                [Winner] text, [Winning Score] float, [Week] text)''')
