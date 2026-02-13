from .display import Display
from .user import User, Role
from .utils import Util
from enum import IntEnum

class MenuType(IntEnum):
    MAIN_MENU = 0
    LIST_USERS = 1
    FIND_USER = 2
    CREATED_USER = 3
    
class MenuSelection:
    def __init__(self, menu: MenuType):
        self.menu = menu
        
    def change(self, new_menu: MenuType):
        self.menu = new_menu

class Menu:
    @staticmethod
    def main_menu(user: User):
        while True:
            Display.display_menu()
            choice = Display.ask_main_menu(len(MenuType))
            match(choice):
                case MenuType.LIST_USERS.value:
                    users = user.list()
                    Menu.list_users(user, users)
                case MenuType.FIND_USER.value:
                    Menu.find_user(user)
                case MenuType.CREATED_USER.value:
                    data = Display.ask_create_user()
                    # Get the password from the user and generate a random one if the user doesn't want to set a password
                    if not data["password"]:
                        data["password"] = Util.generate_password(12)
                        # Display the generated password to the user, don't put in production, it's just for testing
                        print(f"Generated password: {data['password']}")
                    username = User.generate_username(data["firstname"], data["name"])
                    data["email"] = Util.generate_email(username)
                    User.create(data["firstname"],
                        data["name"],
                        data["region"],
                        username,
                        data["email"],
                        Role.USER,
                        data["password"]
                    )
                    Display.user_created()
                case 4:
                    print("\nBye")
                    return True
                
    @staticmethod
    def list_users(user: User, users_list: list[User]):
        chunks = [users_list[i:i+9] for i in range(0, len(users_list), 9)]
        for i, value in enumerate(chunks):
            Display.display_users(value, i, len(chunks))
            choice = Display.ask_select_users(len(value), i == len(chunks) - 1)
            match(choice):
                case x if x in list(map(str, range(1, len(value) + 1))):
                    Menu.user(user, User.from_row(value[int(choice) - 1]))
                    break
                case "0":
                    break
                case "n":
                    continue
    
    @staticmethod
    def find_user(user: User):
        print("\n--- FIND USER ---")
        choice = Display.ask_enum_choice()
        if choice == 0:
            return
        search = input("Search: ").strip().lower()
        users = User.find({User.SEARCHABLE_FIELD[choice]: search})
        if not users:
            print("No user found")
            return
        Menu.list_users(user, users)

    @staticmethod
    def user(user: User, selected_user: User):
        Display.display_user(selected_user)
        choice = Display.ask_user()
        
        match(choice):
            case(1):
                return Menu.update_user(user, selected_user)
            case(2):
                confirm = input("Are you sure you want to delete this user? (y/n): ").strip().lower()
                if confirm.lower() == "y":
                    if (selected_user.role == Role.SUPER_ADMIN and user.role != Role.SUPER_ADMIN) or \
                       (selected_user.role == Role.SUPER_ADMIN and user.id == selected_user.id):
                        print("You are not authorized to delete a super admin user.")
                        return True
                    if selected_user.role == Role.ADMIN and user.role != Role.SUPER_ADMIN:
                        print("You are not authorized to delete an admin user.")
                        return True
                    selected_user.delete()
                    print("User deleted successfully")
                return True
            case(3):
                return True
            
    @staticmethod
    def update_user(user:User, updated_user: User):
        Display.diplay_update_user()
        while True:
            match(Display.ask_update_user()):
                case 0:
                    break
                case 1:
                    new_firstname = input("Insert the new firstname\n").strip().lower()
                    updated_user.firstname = new_firstname
                    updated_user.username = User.generate_username(new_firstname, updated_user.name)
                    updated_user.email = Util.generate_email(updated_user.username)
                case 2:
                    new_name = input("Insert the new name\n").strip().lower()
                    updated_user.name = new_name
                    updated_user.username = User.generate_username(updated_user.firstname, new_name)
                    updated_user.email = Util.generate_email(updated_user.username)
                case 3:
                    # si on a envie rajouter une constante qui permet de chosir des regions fix
                    # d'ailleurs on pourrait lock le choix des regions dans la db
                    new_region = input("Insert the new region\n").strip().lower()
                    updated_user.region = new_region
                case 4:
                    if user.role < Role.SUPER_ADMIN:
                        print("Unauthorized access")
                        continue
                    new_role = Menu.update_role_user(user, updated_user)
                    if not new_role == -1:
                        updated_user.role = Role(new_role)
        updated_user.save()     
        return True
    
    @staticmethod
    def update_role_user(user: User, updated_user: User):
        Display.display_role_user()
        new_role = Display.ask_role_user()
        if new_role == -1:
            return -1
        return new_role
        
    @staticmethod
    def created_user():
        return False