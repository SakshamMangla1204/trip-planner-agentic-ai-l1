import logging
import sys
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


main_logger = setup_logger('main')
graph_logger = setup_logger('graph')
travel_logger = setup_logger('travel_agent')
hotel_logger = setup_logger('hotel_agent')
food_logger = setup_logger('food_agent')
activity_logger = setup_logger('activity_agent')
budget_logger = setup_logger('budget_agent')