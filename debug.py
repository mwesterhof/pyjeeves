import sqlite3


con = sqlite3.connect('jeeves.db')
cursor = con.cursor()


while True:
    inp = raw_input()
    if inp == 'fetch':
        print cursor.fetchall()
    elif inp == 'commit':
        con.commit()
    elif inp == 'desc':
        print cursor.description
    else:
        cursor.execute(inp)
