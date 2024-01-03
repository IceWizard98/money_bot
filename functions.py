import json
import logging
import os

logger = logging.getLogger()


def check_new_user(user_handler: str, chat_id: int) -> None:
    file_name = os.environ['USERS_FILE_NAME']

    if not file_name:
        logger.error("MISS CONFIGURATION, USERS_FILE_NAME environment")
        print("MISS CONFIGURATION, USERS_FILE_NAME environment")

    user_list = {}
    if os.path.isfile(file_name) and os.stat(file_name).st_size > 0:
        user_list = json.load(open(file_name, 'r'))

    if user_handler not in user_list:
        user_list[user_handler] = {"chat_id": chat_id, "amount": 0}
        json.dump(user_list, open(file_name, 'w'))


def load_users():
    file_name = os.environ['USERS_FILE_NAME']

    if not file_name:
        logger.error("MISS CONFIGURATION, USERS_FILE_NAME environment")
        print("MISS CONFIGURATION, USERS_FILE_NAME environment")

    user_list = {}
    if os.path.isfile(file_name) and os.stat(file_name).st_size > 0:
        user_list = json.load(open(os.environ['USERS_FILE_NAME'], 'r'))

    return user_list


def add_amount_to_user( handler: str, amount: float ):
    users = load_users()

    if handler not in users:
        return

    users[handler]["amount"] += amount
    json.dump(users, open(os.environ['USERS_FILE_NAME'], 'w'))


def load_transactions():
    file_name = os.environ['TRANSACTIONS_FILE_NAME']

    if not file_name:
        logger.error("MISS CONFIGURATION, USERS_FILE_NAME environment")
        print("MISS CONFIGURATION, USERS_FILE_NAME environment")

    transactions = []
    if os.path.isfile(file_name) and os.stat(file_name).st_size > 0:
        transactions = json.load(open(file_name, 'r'))

    return transactions


def write_transaction( transaction: dict ):
    if not transaction:
        return

    transactions = load_transactions()

    transactions.append(transaction)
    json.dump(transactions, open(os.environ['TRANSACTIONS_FILE_NAME'], 'w'))
