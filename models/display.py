import getpass
from .user import Role, User

PAGE_SIZE = 9

class Display:

    @staticmethod
    def display_welcome():
        print("=" * 40)
        print(" Welcome to American Hospital ")
        print("=" * 40)
        print()

    @staticmethod
    def ask_login():
        return input("Login:\n").lower().strip()

    @staticmethod
    def welcome_user(firstname):
        print(f"\nWelcome {firstname} \n")

    @staticmethod
    def display_menu():
        print("\n--- SUPER ADMIN MENU ---")
        print("1. List users")
        print("2. Create user")
        print("3. Delete user")
        print("4. Exit")

    @staticmethod
    # Ajouter en mode csv en gros on a un header avec firstname lastname region etc
    # et ensuite on affiche que les infos du header
    # rajouter un index a cote de chaque user de 1 - 9 pour les selctionner
    def display_users(users, page: int):
        if not users:
            print("\n--- USERS LIST ---")
            print("No users found.\n")
            return

        total = len(users)

        headers = ["Firstname", "Name", "Username", "Email", "Region","Role"]

        start = page * PAGE_SIZE
        end = start + PAGE_SIZE

        print("\n--- USERS LIST ---")

        rows = [
            [u.firstname, u.name, u.username, u.email, u.region, Role(u.role)] for u in users
        ]

        col_widths = [
            max(len(row[i]) for row in ([headers] + rows)) for i in range(len(headers))
        ]

        header_line = " | ".join(
            headers[i].ljust(col_widths[i]) for i in range(len(headers))
        )
        print(header_line)
        print("-" * len(header_line))

        for row in rows:
            print(
                " | ".join(
                    row[i].ljust(col_widths[i]) for i in range(len(row))
                )
            )

        print(f"\nPage {page + 1} / {((total - 1) // PAGE_SIZE) + 1}")
        
    @staticmethod
    def display_user(user: User):
        # Rajouter les infos du user prorement, ensuite le menu 1) Update, 2)Delete 3)Exit
        print("1)Update,2)Delete,3)exit")
    
    @staticmethod
    def diplay_update_user():
        #Peut etre changer d'une autre facon comment c'est display
        text_to_display = ""
        for i, value in User.UPDATABLE_FIELD:
            text_to_display += f"#{i})#{value} "
        print(text_to_display + "0) exit/save")
    
    @staticmethod
    def display_role_user():
        for i, role in enumerate(
            [r for r in Role if r != Role.SUPER_ADMIN],
            start=1
        ):
            print(f"{i}) {role.name.title()}")
        print("0) Exit")

    @staticmethod
    def ask_create_user():
        print("\n--- CREATE USER ---")
        return {
            "firstname": input("Firstname: ").strip().lower(),
            "name": input("Name: ").strip().lower(),
            "region": input("Region: ").strip().lower(),
            "password": getpass.getpass("Password (leave empty to generate a random one): ")
        }

    @staticmethod
    def user_created():
        print("User created successfully\n")

    # Vraiment utile?
    @staticmethod
    def user_deleted():
        print("User deleted successfully\n")

    @staticmethod
    def ask_main_menu(number_of_choice: int):
        valid_inputs = list(range(1, number_of_choice + 1))
        print("Choose a options:")
        user_input = None
        while not user_input in valid_inputs:
            if not user_input is None:
                print("Invalid input")
            user_input = int(input(f"[1-{number_of_choice}]").strip())
        return user_input

    @staticmethod
    # a verifier
    def ask_select_users(users_number: int):
        valid_inputs = list(map(str, range(0, users_number + 1)))
        text = f"Choose users [1-{users_number}], 0 Exit"
        if users_number is 9:
            text += ", (N) Next page"
            valid_inputs += ["n"]
        print(text)
        user_input = None
        while not user_input in valid_inputs:
            if not user_input is None:
                print("Invalid input")
            user_input = input("Choose users to get the options of him").strip().lower()
        return user_input
    
    @staticmethod
    def ask_user():
        valid_inputs = list(range(1, 4))
        user_input = None
        while not user_input in valid_inputs:
            if not user_input is None:
                print("Invalid input")
            user_input = int(input("[1-3]:").strip())
        return user_input
    
    @staticmethod
    def ask_update_user():
        valid_inputs = list(range(0, len(User.UPDATABLE_FIELD) + 1))
        user_input = None
        while not user_input in valid_inputs:
            if not user_input is None:
                print("Invalid input")
            user_input = int(input(f"[0-#{len(User.UPDATABLE_FIELD)}]").strip())
        return user_input
    
    @staticmethod
    def ask_role_user():
        valid_inputs = list(range(0, len(Role) + 1))
        user_input = None
        while not user_input in valid_inputs:
            if not user_input is None:
                print("Invalid input")
            user_input = int(input(f"[0-#{len(Role) + 1}]").strip())
        return user_input
    
    @staticmethod
    def ask_enum_choice():
        valid_inputs = []
        for key, value in User.SEARCHABLE_FIELD.items():
            print(f"{key}: {value}")
            valid_inputs.append(key)
        print("0: Exit")
        valid_inputs.append(0)
        user_input = None
        while not user_input in valid_inputs:
            if not user_input is None:
                print("Invalid input")
            user_input = int(input(f"Choose an option [{', '.join(map(str, valid_inputs))}]: ").strip())
        return user_input or 0