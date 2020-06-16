import pandas as pd
import string
import logging
import re

COUNT = 0

class Preprocessor:
    def __init__(self, data_path, filename):
        self.df = pd.read_csv(data_path)
        self.ESCAPES = ''.join([chr(char) for char in range(1, 32)])
        self.filename = filename
        self.COUNT = 0

    def remove_punctuation_and_escapes(self, column_to_clean='readme'):
        print('Removing punctuations...')
        for i in range(len(self.df[column_to_clean])):
            self.df[column_to_clean][i] = self.df[column_to_clean][i] \
                .translate(str.maketrans(self.ESCAPES, ' ' * len(self.ESCAPES))) \
                .translate(str.maketrans('', '', string.punctuation))

    def findCodeBlocks(self, githubFlavoredMarkdown):
        try:
            print(f'finding all code blocks for index {self.COUNT} ...')
            if self.COUNT == 68:
                print(githubFlavoredMarkdown)
            self.COUNT += 1
            return re.findall(r'```(?:[^`]+|`(?!``))*```', githubFlavoredMarkdown)
        except:
            print('error')

    def delete_code_blocks(self, readme):
        codes = self.findCodeBlocks(readme)
        for code in codes:
            readme = readme.replace(code, "")
        return readme

    def bulk_delete_code_blocks(self, column_to_clean='readme'):
        print('Deleting code blocks...')
        self.df[column_to_clean].apply(self.delete_code_blocks)

    def delete_redundent_spaces(self, readme):
        return ' '.join(readme.split())

    def bulk_delete_redundent_spaces(self, column_to_clean='readme'):
        print('Deleting redundent spaces...')
        self.df[column_to_clean].apply(self.delete_redundent_spaces)

    def preprocess(self):
        print('preprocessing data...')
        try:
            self.bulk_delete_code_blocks()
            self.remove_punctuation_and_escapes()
            self.bulk_delete_redundent_spaces()

        except FileNotFoundError:
            logging.error(FileNotFoundError)

    def export(self):
        print('exporting')
        self.df.to_csv(
            f'/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/test_cleaned_data/{self.filename}'
        )


if __name__ == '__main__':
    train_preprocessor = Preprocessor(
        '/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/original_data/train.readme_data.csv',
        'train.cleaned_readme_data.csv'
    )
    eval_preprocessor = Preprocessor(
        '/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/original_data/valid.readme_data.csv',
        'valid.cleaned_readme_data.csv'
    )
    test_preprocessor = Preprocessor(
        '/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/original_data/test.readme_data.csv',
        'test.cleaned_readme_data.csv'
    )

    preprocessors = [train_preprocessor, eval_preprocessor, test_preprocessor]

    for preprocessor in preprocessors:
        preprocessor.preprocess()
        preprocessor.export()

