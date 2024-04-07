import socket
import json
import selectors2 as selectors
from constants import items as all_items, State
from db import get_account, buy_item, sell_item

sel = selectors.DefaultSelector()
current_accounts = []


def accept(server):
    conn, addr = server.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def handle_logout(server, nickname):
    current_accounts.remove(nickname)
    answer = json.dumps({
        "login_status": False,
        "data": None,
    })
    server.sendall(answer)


def send_answer(server, credits, items):
    answer = json.dumps({
        "credits": credits,
        "items": items,
    })
    server.sendall(answer)


def handle_buy_item(server, nickname, item):
    items, credits = buy_item(nickname, item)
    send_answer(server, credits, items)


def handle_sell_item(server, nickname, item):
    items, credits = sell_item(nickname, item)
    send_answer(server, credits, items)


def read(server):
    try:
        while True:
            client_message = json.loads(server.recv(1024))
            state_name, nickname, option = (client_message.get('state'), client_message.get('nickname'),
                                            client_message.get('option'))

            if option == "CHECK_CONNECTION":
                answer = json.dumps({
                    "connection_status": True,
                })
                server.sendall(answer)

            if State[state_name] == State.LOGIN:
                if nickname not in current_accounts:
                    nickname, credits, items = get_account(nickname)
                    answer = json.dumps({
                        "login_status": True,
                        "data": {
                            "nickname": nickname,
                            "credits": credits,
                            "items": items,
                            "all_items": all_items,
                        }
                    })
                    current_accounts.append(nickname)

                else:
                    answer = json.dumps({
                        "login_status": False,
                        "data": None,
                    })

                server.sendall(answer)

            if State[state_name] == State.GAME_SESSION:
                option = client_message.get('option')

                if option == 'LOGOUT':
                    handle_logout(server, nickname)

                item = client_message.get('item')
                if option == 'BUY_ITEM':
                    handle_buy_item(server, nickname, item)

                if option == 'SELL_ITEM':
                    handle_sell_item(server, nickname, item)

    except Exception:
        pass


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('localhost', 2000)
    server.bind(address)
    server.listen(100)
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, accept)
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)

start_server()
