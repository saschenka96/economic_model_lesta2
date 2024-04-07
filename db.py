from models import *
from constants import delta_credits, items


def get_account(account_nickname):
    with db:
        account = Accounts.select().where(Accounts.nickname == account_nickname)
        if not account:
            Accounts.insert(nickname=account_nickname, credits=delta_credits, items='').execute()
            return account_nickname, delta_credits, ''
        else:
            account[0].credits += delta_credits
            account[0].save()
            return account[0].nickname, account[0].credits, account[0].items


def buy_item(account_nickname, item):
    with db:
        account = Accounts.select().where(Accounts.nickname == account_nickname)[0]
        account.credits -= items.get(item)
        account.items += item + " "
        account.save()
        return account.items, account.credits


def sell_item(account_nickname, item):
    with db:
        account = Accounts.select().where(Accounts.nickname == account_nickname)[0]
        account.credits += items.get(item)
        my_items = account.items.split(" ")
        my_items.remove(item)
        account.items = " ".join(my_items)
        account.save()
        return account.items, account.credits


def create_tables():
    with db:
        db.create_tables([Accounts])


create_tables()
