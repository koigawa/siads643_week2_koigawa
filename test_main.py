""" This module performs unit testing on a couple to functions """
import os
import tempfile
import unittest
import pandas as pd
from load import load_csv_data, get_tournament_data
from preprocess_clean import (
    get_goal_diff,
    get_result)

class TestMain(unittest.TestCase):
    """ This class inherits from TestCase for unit testing """

    def setUp(self):
        """ This is for setting up dataframe for testing """
        # # Creates a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_csv_file:
            temp_csv_file.write(
                "date,home_team,away_team,home_score,away_score,tournament,city,country,"\
                "neutral\n2022-11-21,Senegal,Netherlands,0,2,FIFA World Cup,Doha,Qatar,True\n")
            self.temp_file = temp_csv_file.name

    def tearDown(self):
        """ This is for deleting dataframe after unit testing """
        # Removes temporary CSV file after testing
        os.remove(self.temp_file)

    def test_load(self):
        """ This is for testing imported functions from load.py """
        df = load_csv_data(self.temp_file)
        self.assertIsInstance(df, pd.DataFrame)
        df = get_tournament_data('FIFA World Cup', df)
        self.assertEqual(df.iloc[0].tournament, 'FIFA World Cup')

    def test_preprocess_clean(self):
        """ This is for testing imported cleaning functions from preprocess_clean.py """
        df = get_tournament_data(
            'FIFA World Cup', load_csv_data(
                self.temp_file))
        self.assertEqual(get_result(df.iloc[0], "away"), 3)
        self.assertEqual(get_goal_diff(df.iloc[0], "away"), 2)


if __name__ == '__main__':
    unittest.main()
