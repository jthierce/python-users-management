import hashlib

class Util:
    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def check_password(plain, stored_hash):
        return Util.encrypt_password(plain) == stored_hash