import asyncio
import logging
from handlers import dp, bot, router


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    print('All rights reserved, created by @IceWizard88')
    print('The bot is working...')

    log_format = '%(levelname)s: %(asctime)s: %(message)s '
    logging.basicConfig(filename='bot.log', level='INFO', format=log_format)
    logger = logging.getLogger()
    asyncio.run(main())
