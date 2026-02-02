from enum import IntEnum
from dataclasses import dataclass

class Role(IntEnum):
    USER = 0
    ADMIN = 1
    SUPER_ADMIN = 2

@dataclass
class User:
    def __init__(self, firstname, name, region):
        self.name = name
        self.firstname = firstname
        self.region = region
    
    def create():
        pass
    
    def list(name, firstname):
        pass
    
    def delete():
        pass
    
    def update(firstname, name, password, region, email, username):
        pass
    
    @classmethod
    def login(login, password):
        pass
    