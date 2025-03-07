import unittest
import pandas as pd
###########################################################################
class TestDataLoading(unittest.TestCase):
    def test_data_loading(self):
        social = pd.read_csv('Time-Wasters on Social Media.csv')
        data = pd.DataFrame(social)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)

###########################################################################

class TestDataExploration(unittest.TestCase):
    def setUp(self):
        self.social = pd.read_csv('Time-Wasters on Social Media.csv')
        self.data = pd.DataFrame(self.social)

    def test_data_head(self):
        head_data = self.data.head()
        self.assertEqual(len(head_data), 5)

    def test_data_info(self):
        info_output = self.data.info()
        self.assertEqual(len(self.data.columns), 31)
        
class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        return pd.read_csv(self.file_path)

class DataExplorer:
    def __init__(self, data):
        self.data = data

    def get_head(self, n=5):
        return self.data.head(n)

    def get_info(self):
        return self.data.info()

    def get_describe(self):
        return self.data.describe()

###########################################################################

class DataCleaner:
    def __init__(self, data):
        self.data = data

    def drop_columns(self, columns):
        return self.data.drop(columns, axis=1)

    def handle_missing_values(self):
        return self.data.dropna()

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def analyse_the_plot(self, time_spent, category, engagement, no_of_videos_watched, scroll_rate):
        pass

###########################################################################

data_loader = DataLoader('Time-Wasters on Social Media.csv')
data = data_loader.load_data()

data_explorer = DataExplorer(data)
print(data_explorer.get_head())

data_cleaner = DataCleaner(data)
cleaned_data = data_cleaner.drop_columns(['UserID', 'Video ID'])

data_analyzer = DataAnalyzer(cleaned_data)
data_analyzer.analyse_the_plot('Total Time Spent', 'Gender', 'Engagement', 'Number of Videos Watched', 'Scroll Rate')

class TestIntegration(unittest.TestCase):
    def test_integration(self):
        data_loader = DataLoader('Time-Wasters on Social Media.csv')
        data = data_loader.load_data()

        data_explorer = DataExplorer(data)
        head_data = data_explorer.get_head()
        self.assertEqual(len(head_data), 5)

        data_cleaner = DataCleaner(data)
        cleaned_data = data_cleaner.drop_columns(['UserID', 'Video ID'])
        self.assertEqual(len(cleaned_data.columns), 29)


if __name__ == '__main__':
    unittest.main()