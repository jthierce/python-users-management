from enum import IntEnum
from dataclasses import dataclass
from typing import Optional
import sqlite3
from .utils import Util
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

    def list(self):
        if (self.role < int(Role.ADMIN)):
            print("Unhautorized access")
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT *
            FROM users
            ORDER BY name, firstname
        """)
        row = cur.fetchall()
        return row
    
    def delete(self):
        pass
    
    def update(self, firstname, name, password, region, email, username):
        pass
    
    def create(self):
        pass
    
    @staticmethod
    def login_admin(username: str, custom_message = "Invalid password, retry"):
        limit_time = datetime.datetime.now() - datetime.timedelta(hours=8)
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            cur.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            AND role >= ?
            AND(
                blocked_at IS NULL
                OR blocked_at <= ?
            )
            LIMIT 1
            """, (username, int(Role.ADMIN), limit_time))

            row = cur.fetchone()
            if row is None:
                return None
            same_password = False
            for _ in range(3):
                password = getpass.getpass("Password:\n")
                same_password = Util.check_password(password, row["password"])
                if not same_password:
                    print(custom_message)
                else:
                    break
            if not same_password:
                now = datetime.datetime.now()
                cur.execute(
                    "UPDATE users SET blocked_at = ? WHERE id = ?",
                    (now, row["id"])
                )
                con.commit()
                return -1
            
            return User.from_row(row)
        finally:
            con.close()
    
    @classmethod
    def from_row(cls, row):
        return cls(
            row["id"],
            row["firstname"],
            row["name"],
            row["region"],
            row["username"],
            row["email"],
            row["role"],
            row["blocked_at"],
        )