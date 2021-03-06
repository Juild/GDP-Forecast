#!/usr/bin/env python
import os
import sys
import logging
import argparse
import pickle
from datetime import datetime
from utils import config, io, models
logging.basicConfig(
    filename=os.path.join(config.LOGS_PATH, datetime.now().strftime('cli_%Y-%m-%d_%H:%M:%S.log')),
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "task", 
    choices=["train", "predict", "country"], 
    help="Task to be performed", 
)
parser.add_argument(
    "-year", 
    choices=[str(year) for year in range(1981, 2011 + 1)],
    help="Year to be predicted",
    default="2010"
)


if __name__ == "__main__":
    args = parser.parse_args() 
    if args.task == "train":
        logging.info("Training")
        predictor = models.GDPGrowthPredictor(max_depth=9, learning_rate=0.01, subsample=0.8, n_estimators=1000)
        predictor.training_dataset = config.DATABASE_PATH
        predictor.train()
        predictor.save()
    if args.task == "predict":
        if args.year != None:
            logging.info("Predicting")
            predictor = io.load()
            y_pred = predictor.predict(year=int(args.year))
        else:
            sys.stderr.write("Please, provide a year to perform a prediction on\n")
            sys.stderr.flush()
