import os
from typing import Optional
from models import user
from models.user import User
from models.display import Display
from models.menu import Menu, MenuSelection, MenuType

MAX_ATTEMPTS = 3
DB_PATH = "db/Patient-First.db"

def main():
    if not os.path.isfile(DB_PATH):
        print("The db doesn't exist, pls launch initialisation.py before")
        return 0

    Display.display_welcome()

    attempts = 0
    user: Optional[User | int] = None

    # Bloc login admin
    while attempts < MAX_ATTEMPTS and user is None:
        username = Display.ask_login()
        user = User.login_admin(username)

        if user is None:
            attempts += 1
            remaining = MAX_ATTEMPTS - attempts
            if remaining > 0:
                print(f"[ERROR] Login failed. {remaining} put the correct login or your account will be block .\n")
            else:
                print("[SECURITY] Too many failed attempts. Access denied.\n")
                return 0
        elif user == -1:
            print("[SECURITY]Too many fail on password attemps. The account is blocked")
    if not user or user == -1:
        return 0
    Display.welcome_user(user.firstname)
    Menu.main_menu(user)
    return 0


if __name__ == "__main__":
    main()