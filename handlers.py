import logging
import os
import time
import functions
import keyboard

from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.paginator          import Paginator
from aiogram.enums          import ParseMode
from aiogram.filters        import CommandStart
from aiogram.types          import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram                import types, Dispatcher, F, Router
from aiogram                import Bot
from dotenv                 import load_dotenv
from datetime               import datetime

load_dotenv()

TOKEN                = os.environ['BOT_TOKEN']
TOKEN_ICON           = os.environ.get('TOKEN_ICON')
NEGATIVE_AMOUNT      = os.environ.get('NEGATIVE_AMOUNT')
DATE_FORMAT          = os.environ.get('DATE_FORMAT')
PRIVATE_TRANSACTIONS = os.environ.get('PRIVATE_TRANSACTION')

if not TOKEN_ICON:
    TOKEN_ICON = ''

logger = logging.getLogger()
dp     = Dispatcher()
bot    = Bot(TOKEN, parse_mode=ParseMode.HTML)
router = Router(name="router")


@router.message(CommandStart())
@router.message(F.text.regexp(rf"{keyboard.btn_home['command']}"))
async def command_start_handler(message: Message) -> None:

    functions.check_new_user(message.from_user.username, message.from_user.id)

    keyboard_send = keyboard.main_keyboard()

    if not message.from_user.username:
        await message.answer("Hi, if you want to use this bot, please set your username in telegrm settings, then click `/start`.",)
        return

    await (message.answer
    (
        f"Hi, "
        f"{hbold(message.from_user.username)}!\n\n"
        f"This bot will help you to manage transactions between your group of friends\n",
        reply_markup=keyboard_send
    ))


@router.message(F.text.regexp(rf"{keyboard.command_send['command']}").as_('params'))
async def command_send_to_user_handler(message: Message, params) -> None:

    if not params.group('handler'):
        await message.answer( 'Missing user handler' )
        return

    receiver = params.group('handler')

    users = functions.load_users()

    if receiver not in users:
        await message.answer('This user is not registered')
        return

    if receiver == message.from_user.username:
        await message.answer('You are trying to sand money to your account')
        return

    if not params.group('amount'):
        await message.answer('Missing amount')
        return

    amount = str(params.group('amount'))
    amount = amount.replace(',', '.')
    amount = float(amount)

    if amount > users[message.from_user.username]['amount'] and not NEGATIVE_AMOUNT:
        await message.answer(f'You don\'t have enough tokens to send {amount}{TOKEN_ICON}')
        return

    description = ''

    if 'description' in params.groupdict():
        description = params.group('description')

    if description:
        description = description.strip()
    else:
        description = ''

    functions.add_amount_to_user( receiver, amount )
    functions.add_amount_to_user( message.from_user.username, amount * -1 )

    functions.write_transaction( {'receiver': receiver, "sender": message.from_user.username,'amount': amount, "description": description, "date": time.time()} )

    await bot.send_message(users[receiver]['chat_id'], f"You have received {amount}{TOKEN_ICON} from {message.from_user.username}\n\n<b>Description:</b>\n{description}")
    await message.answer(f"Amount sent to <b>{receiver}: {amount}{TOKEN_ICON}</b>\n\n<b>Description:</b>\n{description}")


@router.message(F.text.regexp(rf"{keyboard.btn_send_example['command']}"))
async def command_send_example_handler(message: Message) -> None:
    await message.answer(f"Send a message that meet the following example: \n\n<code>send user_handler 12 description</code>")


@router.message(F.text.regexp(rf"{keyboard.btn_get_all_users['command']}"))
async def command_show_all_users_handler(message: Message) -> None:
    user_list = functions.load_users()
    to_send   = ''

    for key in user_list:
        to_send += f'<code>{key}</code> {user_list[key]["amount"]}{TOKEN_ICON}\n'

    await message.answer(to_send)


@router.message(F.text.regexp(rf"{keyboard.btn_admin_add_amount_command['command']}").as_('params'))
async def command_add_amount_handler(message: Message, params) -> None:

    users = functions.load_users()

    if 'admin' not in users[message.from_user.username] or not users[message.from_user.username]['admin']:
        return

    receiver = params.group('handler')

    if receiver not in users:
        await message.answer('This user is not registered')
        return

    if not params.group('amount'):
        await message.answer('Missing amount')
        return

    amount = float(params.group('amount'))

    if amount < 0 and not NEGATIVE_AMOUNT:
        await message.answer('Cannot add negative amount to users, set <code>NEGATIVE_AMOUNT</code> in .env file to '
                             'enable negative amounts')
        return

    functions.add_amount_to_user(receiver, amount)

    await bot.send_message(users[receiver]['chat_id'], f"You have received {amount}{TOKEN_ICON}")
    await message.answer(f"Amount added to <b>{receiver}: {amount}{TOKEN_ICON}</b>")


@router.message(F.text.regexp(rf"{keyboard.btn_get_transactions['command']}").as_('params'))
async def command_get_transactions_handler(message: Message) -> None:
    transactions = functions.load_transactions()

    total_transactions = len(transactions)
    if total_transactions < 1:
        await message.answer('No transactions')
        return

    pagination = Paginator(
        prev_btn='◀️',
        next_btn='▶️',
        router=router,
        items=[],
        key='transaction_paginated'
    )

    range_i = reversed(range(max(total_transactions-50, 0), total_transactions))

    for index in range_i:
        transaction = transactions[index]

        if transaction['sender'] == message.from_user.username or  transaction['receiver'] == message.from_user.username:
            pagination.items.append(
                f"<b>To:</b> <code>{transaction['receiver']}</code> <b>From:</b> <code>{transaction['sender']}</code>\n"
                f"<b>Amount:</b> <em>{transaction['amount']}{TOKEN_ICON}</em>\n\n"
                f"<b>Description:</b> <code>{transaction['description']}</code>\n\n\n"
                f"<b>Date:</b> <code>{datetime.fromtimestamp(transaction['date']).strftime( DATE_FORMAT )}</code>\n\n"
            )

    await message.answer(pagination.get_current_page(), reply_markup=pagination.get_keyboard().as_markup())


@router.message(F.text.regexp(rf"{keyboard.command_request['command']}").as_('params'))
async def command_request_handler(message: Message, params) -> None:

    if not params.group('handler'):
        await message.answer( 'Missing user handler' )
        return

    obligor = params.group('handler')

    users = functions.load_users()

    if obligor not in users:
        await message.answer('This user is not registered')
        return

    if obligor == message.from_user.username:
        await message.answer('You are trying to sand money to your account')
        return

    if not params.group('amount'):
        await message.answer('Missing amount')
        return

    amount = str(params.group('amount'))
    amount = amount.replace(',', '.')
    amount = float(amount)

    if amount > users[obligor]['amount'] and not NEGATIVE_AMOUNT:
        await message.answer(f'{obligor} don\'t have enough tokens to send {amount}{TOKEN_ICON}')
        return

    description = ''

    if 'description' in params.groupdict():
        description = params.group('description')

    if description:
        description = description.strip()
    else:
        description = ''

    builder = InlineKeyboardBuilder()
    builder.button(text='✅', callback_data=f"send {message.from_user.username} {amount} {description}")
    builder.button(text='❌', callback_data=f"deny {message.from_user.username} {amount} {description}")

    await bot.send_message(
        users[obligor]['chat_id'],
        f"{message.from_user.username} has requested {amount}{TOKEN_ICON}\n\n<b>for:</b> <em>{description}</em>",
        reply_markup=builder.as_markup()
    )

    await message.answer(f"You have requested {amount}{TOKEN_ICON} to {obligor}\n\n<b>for:</b> <em>{description}</em>")


@router.callback_query(F.data.regexp(rf"{keyboard.command_send['command']}").as_('params'))
async def command_confirm_request_handler(query: CallbackQuery, params) ->None:
    if not params.group('handler'):
        await query.message.edit_text( text='Missing user handler' )
        return

    receiver = params.group('handler')

    users = functions.load_users()

    if receiver not in users:
        await query.message.edit_text('This user is not registered')
        return

    if receiver == query.from_user.username:
        await query.message.edit_text('You are trying to sand money to your account')
        return

    if not params.group('amount'):
        await query.message.edit_text('Missing amount')
        return

    amount = str(params.group('amount'))
    amount = amount.replace(',', '.')
    amount = float(amount)

    if amount > users[query.from_user.username]['amount'] and not NEGATIVE_AMOUNT:
        await query.message.edit_text(f'You don\'t have enough tokens to send {amount}{TOKEN_ICON}')
        return

    description = ''

    if 'description' in params.groupdict():
        description = params.group('description')

    if description:
        description = description.strip()
    else:
        description = ''

    functions.add_amount_to_user( receiver, amount )
    functions.add_amount_to_user( query.from_user.username, amount * -1 )

    functions.write_transaction( {'receiver': receiver, "sender": query.from_user.username,'amount': amount, "description": description, "date": time.time()} )

    await bot.send_message(users[receiver]['chat_id'], f"You have received {amount}{TOKEN_ICON} from {query.from_user.username}\n\n<b>Description:</b>\n{description}")
    await query.message.edit_text(f"Amount sent to <b>{receiver}: {amount}{TOKEN_ICON}</b>\n\n<b>Description:</b>\n{description}")


@router.callback_query(F.data.regexp(rf"{keyboard.command_deny_request['command']}").as_('params'))
async def command_deny_request_handler(query: CallbackQuery, params) ->None:
    if not params.group('handler'):
        await query.answer( 'Missing user handler' )
        return

    receiver = params.group('handler')

    users = functions.load_users()

    if receiver not in users:
        await query.answer('This user is not registered')
        return

    if receiver == query.from_user.username:
        await query.answer('You are trying to sand money to your account')
        return

    if not params.group('amount'):
        await query.answer('Missing amount')
        return

    amount = str(params.group('amount'))
    amount = amount.replace(',', '.')
    amount = float(amount)

    description = ''

    if 'description' in params.groupdict():
        description = params.group('description')

    if description:
        description = description.strip()
    else:
        description = ''

    await bot.send_message(
        chat_id=users[receiver]['chat_id'],
        text=f"{query.from_user.username} has denied your request of {amount}{TOKEN_ICON}\n\n <b>for</b> <em>{description}</em>"
    )
    await query.message.edit_text(text=f"Request from {receiver} of {amount}{TOKEN_ICON} has been denied")


@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(f"Comando non riconosciuto {message.text}")
