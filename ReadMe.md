# Telegram Transaction Bot

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3-red)](https://github.com/aiogram/aiogram)
[![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg)](https://github.com/IceWizard98/money_bot/issues)

🤖 This Telegram bot allows users to manage transactions between a group of friends. Users can send and receive tokens, view transaction history, and perform administrative functions.

## 🛠️ Setup

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Copy the `.env.example` and call it `.env`
4. Edit the `.env` file with your personal data and preferences:
   The property `NEGATIVE_AMOUNT` enables negative amounts for all users
5. Edit the `keyboard.py.example` script to specify custom regex for each command and rename it to `keyboard.py`

## 🚀 Usage

1. Start the bot by running the main script.
2. Interact with the bot using the following commands:

- `/start`: Start the bot and access the main menu.
- `send user_handler amount description`: Send tokens to a specified user with an optional description.
- `/send_example`: See an example of the send command format.
- `/get_all_users`: View all registered users and their token amounts.
- `/admin_add_amount user_handler amount`: Add tokens to a user's account (admin-only).
- `/get_transactions`: View the most recent 100 transactions.

After the first start, edit the users file and set the `admin` key in the admin's object to be able to add tokens to other users

## ✨ Features

- 💸 **Send Tokens:** Users can transfer tokens to each other with optional descriptions.
- 👥 **View User List:** Check the list of registered users and their token amounts.
- 🔑 **Admin Functionality:** Admins can add tokens to users' accounts.
- 📜 **Transaction History:** View the most recent transactions.

## 🤝 Contributing

Feel free to contribute by opening issues or pull requests.

## 🙏 Acknowledgments

This bot uses the aiogram library for Telegram bot development.

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 👨‍💻 Authors

- [@IceWizard98](https://www.github.com/IceWizard98)
