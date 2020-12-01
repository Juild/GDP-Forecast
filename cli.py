#!/usr/bin/env python
import os
import logging
import argparse
from datetime import datetime

from utils import config, io, models


logging.basicConfig(
    filename=os.path.join(config.LOGS_PATH, datetime.now().strftime('cli_%Y-%m-%d_%H:%M:%S.log')),
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "task", # argv1 only one argument
    choices=["train", "predict", "country"], # choices for argv1
    help="Task to be performed", # message displayed if "python cli.py --help"
)
# You can add here custom optional arguments to your program

if __name__ == "__main__":
    args = parser.parse_args() # gets the arguments "python3  cli.py argv1, argv2 ..."  
    if args.task == "train":
        print("training")
        logging.info("Training")
    if args.task == "predict":
        logging.info("Predinting")
