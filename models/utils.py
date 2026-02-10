import hashlib
import random
import string

class Util:
    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def check_password(plain, stored_hash):
        return Util.encrypt_password(plain) == stored_hash
    
    @staticmethod
    def generate_password(length):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))