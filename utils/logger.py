import logging
logging.basicConfig(filename="angel_bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_info(msg):
    logging.info(msg)
    print(f"ℹ️ {msg}")

def log_error(msg):
    logging.error(msg)
    print(f"⚠️ {msg}")
