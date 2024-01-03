# Telegram Transaction Bot

This Telegram bot allows users to manage transactions between a group of friends. Users can send and receive tokens, view transaction history, and perform administrative functions.

## Setup

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Copy the `.env.example` and call it `.env`
4. Edit the `.env` file with your personal data and preferences:
   The property `NEGATIVE_AMOUNT` enable negative amount for all users
5. Edit the `keyboard.py.example` script to specify custom regex for each command and rename into `keyboard.py`

## Usage

1. Start the bot by running the main script.
2. Interact with the bot using the following commands:

- `/start`: Start the bot and access the main menu.
- `send user_handler amount description`: Send tokens to a specified user with an optional description.
- `/send_example`: See an example of the send command format.
- `/get_all_users`: View all registered users and their token amounts.
- `/admin_add_amount user_handler amount`: Add tokens to a user's account (admin-only).
- `/get_transactions`: View the most recent 100 transactions.

After first start, edit the users file and set the `admin` key in the admin's object to be able to add tokens to other users

## Features

- **Send Tokens:** Users can transfer tokens to each other with optional descriptions.
- **View User List:** Check the list of registered users and their token amounts.
- **Admin Functionality:** Admins can add tokens to users' accounts.
- **Transaction History:** View the most recent transactions.

## Contributing

Feel free to contribute by opening issues or pull requests.

## Acknowledgments

This bot uses the aiogram library for Telegram bot development.

## License

This project is licensed under the [MIT License](LICENSE).
