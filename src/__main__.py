import logging, os
from bot import Bot

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
bot = Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
bot.start_polling()
