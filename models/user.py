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
    
    UPDATABLE_FIELD = ["firstname", "name", "region", "email", "role"]
    SEARCHABLE_FIELD = {
        1: "name",
        2: "firstname",
        3: "email",
        4: "region"
    }

    def list(self):
        if (self.role < int(Role.ADMIN)):
            print("Unhautorized access")
            return []
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
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (self.id,))
        con.commit()
        con.close()
    
    def save(self):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("""
            UPDATE users
            SET firstname = ?, name = ?, region = ?, username = ?, email = ?, role = ?
            WHERE id = ?
        """, (
            self.firstname,
            self.name,
            self.region,
            self.username,
            self.email,
            int(self.role),
            self.id
        ))
        con.commit()
        con.close()

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
            same_password = None
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
    def create(cls, firstname: str, name: str, region: str, username: str, email: str, role: Role, password: str):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        hashed_password = Util.encrypt_password(password)
        cur.execute("""
            INSERT INTO users (firstname, name, region, username, email, role, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (firstname, name, region, username, email, int(role), hashed_password))
        con.commit()
        con.close()

    @staticmethod
    def find(filters: dict):
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query = "SELECT * FROM users"
        if filters:
            query += " WHERE " + " AND ".join([f"{key} LIKE ?" for key in filters.keys()])
        cur.execute(query, [f"%{value}%" for value in filters.values()])
        row = cur.fetchall()
        return row

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