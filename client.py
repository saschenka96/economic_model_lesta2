import socket
import json

from constants import options, State


# client_message = {
#     "state": "",
#     "option": "",
#     "nickname": "",
#     "item": "",
# }


class Client:

    def __init__(self):
        self.socket = None
        self.state = State.LOGIN
        self.user = None

    def send_message(self, client_message):
        try:
            self.socket.sendall(client_message)
            answer = json.loads(self.socket.recv(1024))
            return answer
        except Exception:
            print('SORRY WE CAN\'T CONTINUE YOUR SESSION DUE TO SERVER MISTAKE!')
            self.state = State.LOGIN

    def get_answer(self, nickname="", option="", item=""):
        client_message = json.dumps({
            "state": self.state.name,
            "option": option,
            "nickname": nickname,
            "item": item,
        })
        return self.send_message(client_message)

    def login(self):
        nickname = raw_input("GIVE ME NICKNAME: ")
        nickname = nickname.strip()
        if nickname == "":
            print("SORRY! YOUR NICKNAME CAN\'T BE EMPTY!")
            return
        if self.connect():
            mess = self.get_answer(nickname)
            if mess.get("login_status"):
                account = mess.get("data")
                if account:
                    self.user = account
                    self.state = State.GAME_SESSION
                    print("CONGRATS! YOU SUCCEFULLY LOGINED!\n")
            else:
                print("CAN\'T LOGIN THIS NICKNAME! TRY ANOTHER ONE!")
        else:
            print("SORRY! WE CAN\'T ESTABLISH CONNECT TO SERVER!")

    def logout(self, option, nickname):
        mess = self.get_answer(nickname, option)
        status = mess.get("login_status")
        if not status:
            self.state = State.LOGIN
            print('YOU SUCESSFULLY LOGOUT!')

    def update_fields(self, nickname, option, item=None):
        update_fields = self.get_answer(nickname, option, item)
        if update_fields:
            credits, items = update_fields.get('credits'), update_fields.get('items')
            self.user['credits'] = credits
            self.user['items'] = items
            return True
        return False

    def sell_item(self, option, nickname, item):
        items = self.user.get('items')
        if items == "":
            print('SORRY! YOU HAVEN\'T NOTHING TO SELL!')
            return

        if item == "":
            print('SORRY! YOU TRY TO SELL NOTHING!')
            return

        if item.upper() == "BACK":
            return

        if item not in items:
            print('SORRY! YOU HAVEN\'T THIS ITEM! YOU CAN\'T SELL IT!')
            return

        if self.update_fields(nickname, option, item):
            print('YOU SUCCESSFULLY SOLD ITEM! %s' % item)

    def buy_item(self, option, nickname, item):
        credits = self.user.get('credits')
        all_items = self.user.get('all_items')
        my_items = self.user.get('items')
        if item == "":
            print('SORRY! YOU TRY TO BUY NOTHING!')
            return

        if item.upper() == "BACK":
            return

        if item not in all_items.keys():
            print('SORRY! WE HAVEN\'T THIS ITEM')
            return

        if item in my_items:
            print("SORRY! YOU HAVE %s ALREADY" % item)
            return

        if credits < all_items.get(item):
            print('SORRY! YOU HAVEN\'T ENOUGH CREDITS! TRY TO EARN MORE')
            return

        if self.update_fields(nickname, option, item):
            print ('YOU SUCCEFULLY BOUGHT ITEM %s' % item)

    def handle_trade_options(self, option):
        item = raw_input('WHICH ITEM ? IF YOU WANT TO BACK TO MENU: BACK\n')
        item = item.strip()
        answer = self.get_answer(option="CHECK_CONNECTION")
        if not answer:
            return

        if option == 'BUY_ITEM':
            self.buy_item(option, self.user.get('nickname'), item)

        elif option == 'SELL_ITEM':
            self.sell_item(option, self.user.get('nickname'), item)

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = ('localhost', 2000)
            self.socket.connect(address)
            return True
        except Exception:
            return False

    def handle_options(self, option):
        if option == 'LOGOUT':
            self.logout(option, self.user.get('nickname'))

        elif option == 'BUY_ITEM' or option == 'SELL_ITEM':
            self.handle_trade_options(option)

        elif option == 'ALL_ITEMS':
            print(
                "\n".join(
                    ['%s : %d' % (key, value) for key, value in self.user.get('all_items').items()]
                )
            )

        elif option == "CREDITS":
            print('YOUR CURRENT CREDITS IS: %d\n' % self.user.get('credits'))

        elif option == "MY_ITEMS":
            items = self.user.get('items')
            if items == "":
                print("YOU HAVEN\'T ANY ITEMS. BUY SOMETHING!")
            else:
                print('YOUR CURRENT ITEMS IS: %s\n' % items)

    def start_client(self):
        try:
            while True:
                while self.state == State.LOGIN:
                    self.login()

                while self.state == State.GAME_SESSION:
                    option = raw_input('PLEASE CHOSE NEXT OPTION FROM: \n%s \n' % '\n'.join(options))
                    option = option.upper()

                    answer = self.get_answer(option="CHECK_CONNECTION")
                    if not answer:
                        break

                    if option not in options:
                        print("MISTAKE!")
                        break

                    self.handle_options(option)
        finally:
            self.socket.close()


client = Client()
client.start_client()
