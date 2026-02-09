from .display import Display
from .user import User
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

                new_user = User(
                    firstname=data["firstname"],
                    name=data["name"],
                    region=data["region"],
                    username=data["username"],
                    email=data["email"],
                    role=Role.USER
                )
                new_user.create(data["password"])
                Display.user_created()
            case 4:
                print("\nBye")
                return True
        
    @staticmethod
    def user(user: User, selected_user: User):
        #Rajouter aussi la methode pour ceci
        Display.display_user(user)
        choice = Display.ask_user()
        
        match(int(choice)):
            case(1):
                return Menu.update_user(user, selected_user)
            case(2):
                user.delete_user(selected_user)
                print("User deleted succesfully")
                return True
            case(3):
                return True
            
    @staticmethod
    def update_user(user:User, updated_user: User):
        Display.diplay_update_user()
        match(Display.ask_update_user()):
            case 0:
                return True
            case 1:
                new_firstname = input("Insert the new firstname")
                user.udpate_firstname(updated_user)
                print("Updated firstname succesfully")
                return True
            case 2:
                new_name = input("Insert the new name")
                user.update_name(updated_user)
            case 3:
                # si on a envie rajouter une constante qui permet de chosir des regions fix
                # d'ailleurs on pourrait lock le choix des regions dans la db
                new_region = input("Insert the new region")
                user.update_region(updated_user)
                return True
            case 4:
                new_username = input("Insert the new username")
                user.update_username(updated_user)
                return True
            case 5:
                new_email = input("Insert the new email")
                user.update_email(updated_user)
                return True
            case 6:
                return Menu.update_role_user(user, updated_user)
        return True
    
    @staticmethod
    def update_role_user(user: User, updated_user: User):
        Display.display_role_user()
        new_role = Display.ask_role_user()
        if new_role == 0:
            return True
        User.update_role(updated_user, new_role)
        return True
        
    @staticmethod
    def created_user():
        return False