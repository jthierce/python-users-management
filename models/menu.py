from .display import Display
from .user import User
from enum import IntEnum

class MenuType(IntEnum):
    MAIN_MENU = 0
    CREATED_USER = 1
    LIST_USERS = 2
    USER = 5
    
class MenuSelection:
    def __init__(self, menu: MenuType):
        self.menu = menu
        
    def change(self, new_menu: MenuType):
        self.menu = new_menu

class Menu:
    @staticmethod
    def main_menu(user: User):
        Display.display_menu()
        choice = Display.ask_choice()
        match(int(choice)):
            case 1:
                users = user.list()
                chunks = [users[i:i+9] for i in range(0, len(users), 9)]
                for i, value in chunks:
                    is_last_element = i == len(chunks) - 1
                    Display.display_users(value, i, is_last_element)
                    # rAJOUTER LA METHODE QUI PERMET DE SELECTIONER LE USER OU DE NEXT LA PAGE OU DE QUITTER
                    valid_input = False
                    while not valid_input:
                        choice = Display.choose_users()
                        match(choice):
                            case x if 1 <= int(x) <= 9:
                                return Menu.user(User.from_row(i[int(x)]))
                            case "n":
                                if not is_last_element:
                                    valid_input = True
                            case "0":
                                return True
                            case _:
                                print("Invalid input, retry")
            case 2:
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
            case 3:
                user_id = Display.ask_delete_user()
                u = User(id=user_id)
                u.delete()
                Display.user_deleted()
            case 4:
                print("\nBye")
                break
            case _:
                Display.invalid_choice()
        
    @staticmethod
    def user(user: User):
        #Rajouter aussi la methode pour ceci
        Display.user(user)
        choice = Display.ask_user()
        
        while True
            match(int(choice)):
                case(1):
                    return Menu.update_user()
                case(2):
                    return Menu.Delete_user()
                case(0):
                    return True
                case _:
                    print("Invalide output")
    
                
    @staticmethod
    def created_user():
        return False