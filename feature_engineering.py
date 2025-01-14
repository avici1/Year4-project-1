"""
This module provides feature engineering capabilities for the project. Certain new fields can be produced 
all in order to produce fast and effective predictions
"""

import calendar
from typing import Tuple, List

from pandas import DataFrame, get_dummies, qcut


class FeatureEngineering:
    """
    Base class defining which methods to use.
    """

    def __init__(self, data_frame: DataFrame):
        """
        Base constructor for setting basic variables
        """
        self.data_frame = data_frame

    def create_month_year(self):
        """
        Creates a new property called YearMonth.
        Which is a combination of the month and the year.
        This will be important if we want to showcase data chronologically
        """
        months = list(calendar.month_name)[1:]

        # Conversion to number format for easy graphical representation
        self.data_frame["arrival_date_month"] = self.data_frame[
            "arrival_date_month"
        ].map(lambda m: months.index(m) + 1)

        self.data_frame["arrival_date_year"] = self.data_frame["arrival_date_year"].map(
            lambda y: str(y).split("20")[1]
        )
        # This was joined to give more context on date sensitive answers.
        self.data_frame["YearMonth"] = (
            self.data_frame["arrival_date_year"].astype(str)
            + "/"
            + self.data_frame["arrival_date_month"].astype(str)
        )

    def create_duration(self):
        """
        Creates a new duration property.
        Which combines the days stayin for both the weekend and week days.
        This is particularly important because it gives a good summarised
        and concise measure of the stay of the individual.
        """
        # This is to be able to use the duration.
        self.data_frame["duration"] = (
            self.data_frame["stays_in_weekend_nights"]
            + self.data_frame["stays_in_week_nights"]
        )

    def one_hot_encoding(self, properties):
        """
        This encodes the passed properties to create dummies that are
        exploitable in further domains. This is important especially
        while running algorithms that rely on account numerical values
        """
        self.data_frame = get_dummies(self.data_frame, columns=properties)
        return self.data_frame


    def binning(self, prop:str) -> Tuple[DataFrame, List[str]]:
        """
        Returns a dataframe that contains the newly binned property
        """
        new_prop = f'bin_{prop}'
        self.data_frame[new_prop], bin_edges = qcut(
            self.data_frame[prop],
            10,
            retbins=True,
            labels=False,
            duplicates='drop'
        )
        bin_labels = [f'({bin_edges[i]:.1f}, {bin_edges[i + 1]:.1f})' for i in range(len(bin_edges) - 1)]
        return self.data_frame, bin_labels