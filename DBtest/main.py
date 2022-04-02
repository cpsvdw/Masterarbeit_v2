import sqlite3

con = sqlite3.connect('testdb.db')

cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS manmodels
(id real, brand text, model text, pr real  PRIMARY KEY, weight real, file )
''')

cur.execute('''INSERT OR IGNORE INTO manmodels VALUES
('2', 'MAN', 'TGM', '123985473165', '13-26')''')

con.commit()

for row in cur.execute('''SELECT * FROM manmodels'''):
    print(row)