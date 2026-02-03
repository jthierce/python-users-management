from enum import IntEnum
from dataclasses import dataclass
from typing import Optional
import sqlite3
from utils import Util
import getpass
import datetime

DB_PATH = "db/Patient-First.db"

class Role(IntEnum):
    USER = 0
    ADMIN = 1
    SUPER_ADMIN = 2

@dataclass
class User:
    id: Optional[int] = None
    firstname: str = ""
    name: str = ""
    region: str = ""
    username: str = ""
    email: str = ""
    role: Role = Role.USER
    blocked_at: Optional[str] = None

    
    def get(self, Sname, firstname):
        # check si le user a le droit d'affichier
        pass
    
    def delete(self):
        pass
    
    def update(self, firstname, name, password, region, email, username):
        pass
    
    def create(self):
        pass
    
    @staticmethod
    def login_super_admin(username, custom_message = "Invalid password, retry"):
        limit_time = datetime.datetime.now() + datetime.timedelta(hours=8)
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
        SELECT *
        FROM users
        WHERE username = ?
          AND role = ?
          AND(
            blocked_at IS NULL
            OR blocked_at > ?
          )
        LIMIT 1
        """, (username, int(Role.SUPER_ADMIN), limit_time))

        row = cur.fetchone()
        if row is None:
            return None
        i = 0
        same_password = False
        while(i < 3 and same_password is False):
            password = Util.encrypt_password(getpass.getpass("Password:\n"))
            i += 1
            same_password = password == row["password"]
        if(same_password is False):
            row["blocket_at"] = datetime.datetime.now()
            # la on save la nuvelle data
            cur.execute(save)
            return None
        
        return User(row["id"], row["firstname"], row["name"], row["region"], row["username"], row["email"], row["role"], row["blocket_at"])