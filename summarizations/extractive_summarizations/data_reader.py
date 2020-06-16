import pandas as pd

class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        df = pd.read_csv(self.file_path)
        df.drop('Unnamed: 0', 1)
        print(f'Successfully read csv file')
        print(df)
        return df


