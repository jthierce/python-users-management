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
        Display.display_menu()
        choice = Display.ask_main_menu(len(MenuType))
        match(choice):
            case MenuType.LIST_USERS.value:
                users = user.list()
                chunks = [users[i:i+9] for i in range(0, len(users), 9)]
                for i, value in chunks:
                    Display.display_users(value, i)
                    choice = Display.ask_select_users(len(value))
                    match(choice):
                        case x if x in list(map(str, range(1, len(value) + 1))):
                            return Menu.user(User.from_row(value[int(choice) - 1]))
                        case "0":
                            return True
            case MenuType.FIND_USER.value:
                Menu.find_user()
            case MenuType.CREATED_USER.value:
                data = Display.ask_create_user()
                # Get the password from the user and generate a random one if the user doesn't want to set a password
                if not data["password"]:
                    data["password"] = Util.generate_password(12)
                    print(f"Generated password: {data['password']}")
                User.create(data["firstname"],
                    data["name"],
                    data["region"],
                    data["username"],
                    data["email"],
                    Role.USER,
                    data["password"]
                )
                Display.user_created()
            case 4:
                print("\nBye")
                return True
        
    @staticmethod
    def user(user: User, selected_user: User):
        Display.display_user(user)
        choice = Display.ask_user()
        
        match(int(choice)):
            case(1):
                return Menu.update_user(user, selected_user)
            case(2):
                confirm = input("Are you sure you want to delete this user? (y/n): ")
                if confirm.lower() == "y":
                    if selected_user.role == Role.SUPER_ADMIN and user.role != Role.SUPER_ADMIN:
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
        want_to_stop = False
        while not want_to_stop:
            match(Display.ask_update_user()):
                case 0:
                    want_to_stop = True
                case 1:
                    new_firstname = input("Insert the new firstname")
                    updated_user.firstname = new_firstname
                case 2:
                    new_name = input("Insert the new name")
                    updated_user.name = new_name
                case 3:
                    # si on a envie rajouter une constante qui permet de chosir des regions fix
                    # d'ailleurs on pourrait lock le choix des regions dans la db
                    new_region = input("Insert the new region")
                    updated_user.region = new_region
                case 4:
                    new_username = input("Insert the new username")
                    updated_user.username = new_username
                case 5:
                    new_email = input("Insert the new email")
                    updated_user.email = new_email
                case 6:
                    if user.role < Role.SUPER_ADMIN:
                        print("Unauthorized access")
                        continue
                    new_role = Menu.update_role_user(user, updated_user)
                    if not new_role == 0:
                        updated_user.role = Role(new_role)
        updated_user.save()     
        return True
    
    @staticmethod
    def update_role_user(user: User, updated_user: User):
        Display.display_role_user()
        new_role = Display.ask_role_user()
        if new_role == 0:
            return 0
        return new_role
        
    @staticmethod
    def created_user():
        return False