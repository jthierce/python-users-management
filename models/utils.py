import hashlib

class Util:
    @classmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode()).hexdigest()