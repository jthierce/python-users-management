from .user import Role

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
        return input("Login:\n").lower()
    
    @staticmethod
    def ask_password():
        return input("Password:\n")

    @staticmethod
    def auth_failed():
        print("\n Authentication failed.\n")

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
    def ask_choice():
        return input("Choice: ")

    @staticmethod
    def invalid_choice():
        print(" Invalid choice\n")

    @staticmethod
    # Ajouter en mode csv en gros on a un header avec firstname lastname region etc
    # et ensuite on affiche que les infos du header
    # rajouter un index a cote de chaque user de 1 - 9 pour les selctionner
    # 0 pour quitter et n pour next
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

        # largeur des colonnes
        col_widths = [
            max(len(row[i]) for row in ([headers] + rows)) for i in range(len(headers))
        ]

        # header
        header_line = " | ".join(
            headers[i].ljust(col_widths[i]) for i in range(len(headers))
        )
        print(header_line)
        print("-" * len(header_line))

        # lignes
        for row in rows:
            print(
                " | ".join(
                    row[i].ljust(col_widths[i]) for i in range(len(row))
                )
            )

        print(f"\nPage {page + 1} / {((total - 1) // PAGE_SIZE) + 1}")
        print("n = next page | 0 = quit")

    @staticmethod
    def ask_create_user():
        print("\n--- CREATE USER ---")
        return {
            "firstname": input("Firstname: "),
            "name": input("Name: "),
            "region": input("Region: "),
            "username": input("Username: "),
            "email": input("Email: "),
            "password": input("Password: "),
        }
    
    @staticmethod
    def ask_delete_user():
        print("\n--- DELETE USER ---")
        return input("User ID to delete: ")


    @staticmethod
    def user_created():
        print(" User created successfully\n")

    @staticmethod
    def user_deleted():
        print(" User deleted successfully\n")








#         import shutil
# from getpass import getpass

# class Display:

#     # ------------------------------------------------------------------
#     # Cadre responsive avec texte centré
#     # ------------------------------------------------------------------
#     @classmethod
#     def frame_block(cls, lines):
#         # Largeur du terminal
#         term_width = shutil.get_terminal_size().columns

#         # Longueur max du texte
#         max_len = min(max(len(line) for line in lines), term_width - 6)

#         # Largeur du cadre
#         width = max_len + 4

#         print("*" * width)
#         for line in lines:
#             centered = line.center(max_len)
#             print(f"* {centered} *")
#         print("*" * width)
#         print()

#     # ------------------------------------------------------------------
#     # Workflow Login
#     # ------------------------------------------------------------------
#     @classmethod
#     def display_welcome(cls):
#         cls.frame_block([
#             "Welcome to American Hospital",
#             "",
#             "Entrer votre login :"
#         ])
#         return input("> ")

#     @classmethod
#     def ask_password(cls):
#         cls.frame_block(["Entrer votre mot de passe"])
#         return getpass("> ")

#     @classmethod
#     def auth_success(cls):
#         cls.frame_block(["Authentification reussi"])

#     @classmethod
#     def auth_failed(cls):
#         cls.frame_block(["Authentification échouée"])

#     # ------------------------------------------------------------------
#     # Menus
#     # ------------------------------------------------------------------
#     @classmethod
#     def display_main_menu(cls):
#         cls.frame_block([
#             "MAIN MENU",
#             "",
#             "1. Create User",
#             "2. List User",
#             "3. Find User",
#             "4. Exit"
#         ])
#         return input("> ")

#     @classmethod
#     def display_list_menu(cls):
#         cls.frame_block([
#             "USERS LIST",
#             "",
#             "1. Afficher les utilisateurs (1 par ligne)",
#             "-> username | firstname | email | etc.",
#             "",
#             "2. Afficher 9 utilisateurs maximum",
#             "",
#             "0. Retourner au menu principal"
#         ])
#         return input("> ")

#     @classmethod
#     def display_user_menu(cls, user):
#         cls.frame_block([
#             "USER INFORMATION",
#             "",
#             f"Username : {user['username']}",
#             f"Firstname : {user['firstname']}",
#             f"Email : {user['email']}",
#             "",
#             "1. Update the user",
#             "2. Delete the user",
#             "3. Return to the main menu"
#         ])
#         return input("> ")

# # ----------------------------------------------------------------------
# # Exemple de workflow complet
# # ----------------------------------------------------------------------

# def main():
#     # Identifiants fictifs
#     admin_login = "admin"
#     admin_password = "1234"

#     # Login
#     login = Display.display_welcome()
#     password = Display.ask_password()

#     if login == admin_login and password == admin_password:
#         Display.auth_success()
#     else:
#         Display.auth_failed()
#         return

#     # Menu principal
#     while True:
#         choice = Display.display_main_menu()

#         if choice == "1":
#             Display.frame_block(["Création d'utilisateur (à implémenter)"])

#         elif choice == "2":
#             Display.display_list_menu()

#         elif choice == "3":
#             fake_user = {
#                 "username": "jdoe",
#                 "firstname": "John",
#                 "email": "john@doe.com"
#             }
#             Display.display_user_menu(fake_user)

#         elif choice == "4":
#             Display.frame_block(["Au revoir"])
#             break

#         else:
#             Display.frame_block(["Choix invalide"])

# if __name__ == "__main__":
#     main()