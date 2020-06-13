import pandas as pd
import string
import logging


class Preprocessor:
    def __init__(self, data_path, filename):
        self.df = pd.read_csv(data_path)
        self.ESCAPES = ''.join([chr(char) for char in range(1, 32)])
        self.filename = filename

    def remove_punctuation_and_escapes(self, readme_df, column_to_clean='readme'):
        for i in range(len(readme_df[column_to_clean])):
            logging.info(f'preprocessing the data in the {column_to_clean} column...')
            readme_df[column_to_clean][i] = readme_df[column_to_clean][i] \
                .translate(str.maketrans(self.ESCAPES, ' ' * len(self.ESCAPES))) \
                .translate(str.maketrans('', '', string.punctuation))

    def preprocess(self):
        logging.info('preprocessing data...')
        try:
            self.remove_punctuation_and_escapes(self.df)
        except FileNotFoundError:
            logging.error(FileNotFoundError)

    def export(self):
        logging.info('exporting')
        self.df.to_csv(f'../data/cleaned_data/{self.filename}')


if __name__ == '__main__':
    train_preprocessor = Preprocessor(
        '/Users/vincenthuang/Development/Summer-2020/train.readme_data.csv',
        'train.cleaned_readme_data.csv'
    )
    eval_preprocessor = Preprocessor(
        '/Users/vincenthuang/Development/Summer-2020/valid.readme_data.csv',
        'valid.cleaned_readme_data.csv'
    )
    test_preprocessor = Preprocessor(
        '/Users/vincenthuang/Development/Summer-2020/test.readme_data.csv',
        'test.cleaned_readme_data.csv'
    )

    preprocessors = [train_preprocessor, eval_preprocessor, test_preprocessor]

    for preprocessor in preprocessors:
        preprocessor.preprocess()
        preprocessor.export()

