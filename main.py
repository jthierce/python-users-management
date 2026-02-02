import getpass
from models.user import User
from models.utils import Util
from models.display import Display

Display.welcome()
login = input("Login:\n")
password_encrypted = Util.encrypt_password(getpass.getpass("Password:\n")).hexdigest()
print(password_encrypted)