import asyncio
import logging
from handlers import dp, bot


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('All rights reserved, created by @IceWizard88')
    print('The bot is working...')

    log_format = '%(levelname)s: %(asctime)s: %(message)s '
    logging.basicConfig(filename='bot.log', level='INFO', format=log_format)
    logger = logging.getLogger()
    asyncio.run(main())
