import hashlib

class Util:
    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode()).hexdigest()