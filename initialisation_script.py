import sqlite3
import getpass
import os
# Plus propre d'utiliser sys.exit dans un script que exit, aller voir de la doc si necessaire
import sys
from models.utils import Util

# Constante
DB_PATH = "db/Patient-First.db"

os.makedirs("db", exist_ok=True)

if os.path.isfile(DB_PATH):
    print("The db already exist pls delete if you want to restart the process")
    sys.exit(0)

con = sqlite3.connect(DB_PATH)
con.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    firstname TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    region TEXT NOT NULL,
    password BLOB NOT NULL,
    blocked_at NUMERIC,
    role INTEGER NOT NULL DEFAULT 0
)
""")

# rajouter la creation du super admin 
name = input("Insert the name of the superadmin:\n").strip().lower()
firstname = input("Insert the firstname of the superadmin:\n").strip().lower()

attemp_password = 0
while (attemp_password < 3):
    password = getpass.getpass("Insert password:\n").strip()
    confirm_password = getpass.getpass("Confirm the password:\n").strip()
    if password == confirm_password and len(password) >= 8:
        break
    else:
        attemp_password += 1
        print("Incorrect same password, or length too short")

# Gestion d'erreur sur le mot de passe du super admin
if attemp_password == 3:
    print("Attemp to create password expired, script failed relaunch it\n")
    con.close()
    os.remove(DB_PATH)
    sys.exit(0)

username = firstname[0] + name[0] + name
try:
    con.execute("""
                INSERT INTO users
                (name, firstname, username, email, region, password, role)
                VALUES (?,?,?,?,?,?, 2)
    """, (name.strip(), firstname.strip(), username, username + "@american-hosptial.intranet", 'Paris', Util.encrypt_password(password)))
except Exception as e:
    print("Error in db:\n" + str(e))
    con.close()
    os.remove(DB_PATH)
    sys.exit(0)
print("User created\n")


con.commit()
con.close()