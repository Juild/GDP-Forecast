import sqlite3
import pickle
import pandas as pd
import sys
from xgboost import XGBRegressor
from utils import config, io

class GDPGrowthPredictor(XGBRegressor):
    """
    Class used to predict next year's GDP growth for all of the world countries.

    Attributes
    ----------
    __training_dataset: pandas.DataFrame object
        the dataset used for the training of the model (default is None)
    __prediction_dataset: pandas.DataFrame object
        the dataset used for prediction (default is None)
    __features: pandas.DataFrame object
        features dataset used for trainning
    __target: pandas.DataFrame object
        target dataset used for trainning
    
    Methods:
    ----------
    train(**kwargs)
        trains the model using XGBRegressor.fit method
    predict(year, file_name, **kwargs)
        predicts GDP growth for a given year and dumps the result into a csv file.
    save(file_name):
        serielizes the object into a binary file. 
    """
    __doc__ += XGBRegressor.__doc__
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__training_dataset = None
        self.__prediction_dataset = None
        self.__features = None
        self.__target = None

    def train(self, **kwargs):
        """Trains the model usin XGBRegressor.fit method

        In order to do so, it applies some transformations to the dataset
        and creates the __features  and __target attributes, which will be
        later passed to the XGBRegressor.fit method.
        """

        first_year = self.__training_dataset.index.get_level_values(level=config.YEAR).unique()[0]
        last_year = self.__training_dataset.index.get_level_values(level=config.YEAR).unique()[-1]

        self.__features = self.__training_dataset.drop(index=last_year, level=config.YEAR)
        self.__target = self.__training_dataset.drop(columns=self.__training_dataset.columns.difference([config.GDP_GROWTH]))
        self.__target.drop(index=first_year, level=config.YEAR, inplace=True)

        self.__features.fillna(self.__features.mean(), inplace=True)
        self.__target.fillna(self.__target.mean(), inplace=True)
        
        # set base score for the XGBRegressor
        self.base_score = self.__target.to_numpy().mean()
        sys.stdout.write("Training...")
        sys.stdout.flush()
        super().fit(self.__features.to_numpy(), self.__target.to_numpy(), **kwargs)
        sys.stdout.write(" Done.\n")
    def predict(self, year, file_name=config.SERIALIZED_MODEL, **kwargs):
        """Predicts GDP growth for a given year and dumps the result into a csv file.

        First, the `self.__prediction_dataset` attribute is created, given the `year` 
        passed and then XGBRegressor.predict method is used to predict on new data.

        Parameters:
        ----------
        year : int
            year to perform a prediction on the GDP growth.
        """
        dfs = []
        countries = self.__training_dataset.index.get_level_values(level=config.COUNTRY_CODE).unique()
        for country in countries:
            dfs.append(self.__training_dataset.loc[(country, year - 1)].to_frame().T)
       
        self.__prediction_dataset = pd.concat(dfs)
        self.__prediction_dataset.fillna(self.__prediction_dataset.mean(), inplace=True)
        sys.stdout.write("Predicting...")
        sys.stdout.flush()
        predictions = super().predict(self.__prediction_dataset.to_numpy(), output_margin=True, **kwargs)
        sys.stdout.write(" Done.\n")
        sys.stdout.flush()
        sys.stdout.flush()
        predictions_df = pd.DataFrame.from_dict({f"{config.GDP_GROWTH}_YEAR_{year}": predictions})
        predictions_df[config.COUNTRY_CODE] = self.__features.index.get_level_values(level=config.COUNTRY_CODE).unique()
        predictions_df.set_index(config.COUNTRY_CODE)
        sys.stdout.write("Writing to the database...")
        sys.stdout.flush()
        with sqlite3.connect(config.DATABASE_PATH) as connection:
            predictions_df.to_sql(config.PREDICTIONS_TABLE, connection, if_exists='replace', index = False)
        sys.stdout.write(" Done.\n")
    @property
    def training_dataset(self):
        """Get the training dataset
        
        When setting the `self.__training_dataset` a path to an sqlite3 database is expected.
        Then, the setter performs several cleaning operations on the data, such as: pivoting,
        removing countries with no GDP growth, removing the first 20 years of observations
        for each country (due to excessive NA's) and selecting only the final variables of
        the model. 
        """ 
        return self.__training_dataset

    @training_dataset.setter
    def training_dataset(self, new_dataset):
        sys.stdout.write("Retrieving and saving Dataset as pandas.DataFrame object...")
        sys.stdout.flush()
        df = io.retrieve_training_dataset(new_dataset)
        sys.stdout.write(" Done.\n")
        sys.stdout.flush()
        sys.stdout.write("Pivoting and cleaning DataFrame...")
        sys.stdout.flush()
        df_cleaned = config.clean_and_pivote(df)
        self.__training_dataset = df_cleaned.drop(range(1960, 1980), level=config.YEAR)
        sys.stdout.write(" Done.\n")
        sys.stdout.flush()

    @training_dataset.deleter
    def training_dataset(self):
        sys.stdout.write("Removing dataset...")
        sys.stdout.flush()
        del self.__training_dataset
        sys.stdout.write(" Done.")
        sys.stdout.flush()

    @property
    def prediction_dataset(self):
        return self.__prediction_dataset
    
    @property
    def feautures(self):
        return self.__features
    
    @property
    def target(self):
        return self.__target

    def save(self, file_name=config.SERIALIZED_MODEL):
        pickle.dump(self, open(f"{config.MODELS_PATH}/{file_name}", "wb"))