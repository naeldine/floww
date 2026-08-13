import sqlite3
from floww import charger

data = charger()

conn = sqlite3.connect("floww.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS depenses (id INTEGER PRIMARY KEY, nom TEXT, montant REAL, mois TEXT)""")
cur.execute("""CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY, revenu REAL, objectif_epargne REAL)""")

cur.execute("INSERT INTO config (revenu, objectif_epargne) VALUES (?,?)", (data["revenu"], data["objectif_epargne"]))

for depense in data["depenses"]:
    cur.execute("INSERT INTO depenses (nom, montant, mois) VALUES (?,?,?)", (depense["nom"], depense["montant"], data["mois"]))
conn.commit()
cur.execute("SELECT * FROM depenses")
print(cur.fetchall())
conn.close()    



