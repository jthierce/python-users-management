import os
from typing import Optional
from models.user import User, Role
from models.display import Display

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
    breakpoint()

    # while True:
    #     Display.display_menu()
    #     choice = Display.ask_choice()

    #     if choice == "1":
    #         users = User.get_all()
    #         Display.display_users(users)

    #     elif choice == "2":
    #         data = Display.ask_create_user()

    #         new_user = User(
    #             firstname=data["firstname"],
    #             name=data["name"],
    #             region=data["region"],
    #             username=data["username"],
    #             email=data["email"],
    #             role=Role.USER
    #         )
    #         new_user.create(data["password"])
    #         Display.user_created()

    #     elif choice == "3":
    #         user_id = Display.ask_delete_user()
    #         u = User(id=user_id)
    #         u.delete()
    #         Display.user_deleted()

    #     elif choice == "4":
    #         print("\nBye")
    #         break

    #     else:
    #         Display.invalid_choice()


if __name__ == "__main__":
    main()