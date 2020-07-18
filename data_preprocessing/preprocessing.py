import gfm
import pandas as pd
import string
import logging
import re
import nltk
from nltk.stem import WordNetLemmatizer
from constants.mac import ORIGINAL_DATA_TRAIN, ORIGINAL_DATA_VALID, ORIGINAL_DATA_TEST
from constants.default import OUTPUT_FILE_TRAIN, OUTPUT_FILE_VALID, OUTPUT_FILE_TEST

from bs4 import BeautifulSoup
from interruptingcow import timeout
import ast

COUNT = 0

class Preprocessor:
    def __init__(self, data_path, filename, extractive=False):
        self.df = pd.read_csv(data_path)
        self.ESCAPES = ''.join([chr(char) for char in range(1, 32)])
        self.filename = filename
        self.COUNT = 0
        self.faulty_indices = []
        self.extractive = extractive

    def remove_starting_periods(self, readme):
        if readme.startswith('.'):
            print('removing starting periods...')
            while readme.startswith('.'):
                readme = readme.replace('.', '', 1)
        return readme

    def bulk_remove_starting_periods(self, column_to_clean='readme'):
        self.df[column_to_clean] = self.df[column_to_clean].apply(self.remove_starting_periods)

    def remove_punctuation_and_escapes(self, column_to_clean='readme'):
        print('Removing punctuations...')
        if self.extractive:
            punctuation = string.punctuation.replace('.', '')
        else:
            punctuation = string.punctuation
        for i in range(len(self.df[column_to_clean])):
            self.df[column_to_clean][i] = self.df[column_to_clean][i] \
                .translate(str.maketrans(self.ESCAPES, ' ' * len(self.ESCAPES))) \
                .translate(str.maketrans('', '', punctuation))
        self.bulk_remove_starting_periods()

    def findCodeBlocks(self, githubFlavoredMarkdown):
            self.COUNT += 1
            return re.findall(r'```(?:[^`]+|`(?!``))*```', githubFlavoredMarkdown)

    def delete_code_blocks(self, readme):
        codes = self.findCodeBlocks(readme)
        print(f'Deleting code blocks for index {self.COUNT}')
        for code in codes:
            readme = readme.replace(code, "")
        return readme

    def delete_code_blocks2(self, readme):
        substituted_text = re.sub(r'```.*?```', "", readme, re.MULTILINE, re.DOTALL)
        substituted_text = re.sub(r'`.*?`', "", substituted_text, re.MULTILINE, re.DOTALL)
        return substituted_text

    def to_lower_case(self, readme):
        return readme.lower()

    def bulk_to_lower_case(self, column_to_clean='readme'):
        print('Converting to lower cases')
        self.df[column_to_clean] = self.df[column_to_clean].apply(self.to_lower_case)

    def bulk_delete_code_blocks(self, column_to_clean='readme'):
        print('Deleting code blocks...')
        for i in range(len(self.df[column_to_clean])):
            try:
                with timeout(2, exception=RuntimeError):
                    self.df[column_to_clean][i] = self.delete_code_blocks2(self.df[column_to_clean][i])
            except RuntimeError:
                print('timeout deleting code blocks')
                self.faulty_indices.append(i)

    def write_faulty_index_to_txt_file(self):
        print('writing faulty indices to txt files...')
        with open(f'/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/cleaned_data/incidents'
                  f'/faulty_indices_{self.filename}.txt', 'w+') as fn:
            fn.write(str(self.faulty_indices))

    def delete_redundent_spaces(self, readme):
        readme = re.sub('\t+', ' ', readme)
        return re.sub(' +', ' ', readme)

    def bulk_delete_redundent_spaces(self, column_to_clean='readme'):
        print('deleting redundent spaces...')
        self.df['readme'] = self.df[column_to_clean].apply(self.delete_redundent_spaces)

    def convert_to_html(self, readme):
        return gfm.markdown(readme)

    def get_text_from_html(self, html):
        soup = BeautifulSoup(html)
        for script in soup(['script', 'style']):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def remove_markdown(self, readme):
        self.COUNT += 1
        html = self.convert_to_html(readme)
        readme = self.get_text_from_html(html)
        return readme

    def bulk_remove_markdown(self, column_to_clean='readme'):
        self.COUNT = 0
        for i in range(len(self.df[column_to_clean])):
            try:
                with timeout(2, exception=RuntimeError):
                    self.df[column_to_clean][i] = self.remove_markdown(self.df[column_to_clean][i])
            except RuntimeError:
                print('timeout removing markdown')
                self.faulty_indices.append(i)

    def remove_faulty_rows(self):
        print('removing faulty rows...')
        self.df.drop(self.faulty_indices, inplace=True)

    def convert_purpose_to_sentence(self, purpose):
        words = ast.literal_eval(purpose)
        sentence = ' '.join(words)
        return sentence.translate(str.maketrans('', '', string.punctuation))

    
    def bulk_convert_purpose_to_sentence(self, column_to_clean='purpose'):
        self.df[column_to_clean] = self.df[column_to_clean].apply(self.convert_purpose_to_sentence)
        self.df[column_to_clean] = self.df[column_to_clean].apply(self.delete_redundent_spaces)
        

    # def get_wordnet_pos(self, word):
    #     """Map POS tag to first character lemmatize() accepts"""
    #     tag = nltk.pos_tag([word])[0][1][0].upper()
    #     tag_dict = {"J": wordnet.ADJ,
    #                 "N": wordnet.NOUN,
    #                 "V": wordnet.VERB,
    #                 "R": wordnet.ADV}

    #     return tag_dict.get(tag, wordnet.NOUN)


    # def lemmatize(self, readme):
    #     wordnet_lemmatizer = WordNetLemmatizer()

    #     punctuations=string.punctuation
    #     words = nltk.word_tokenize(readme)
    #     for word in words:
    #         if word in punctuations:
    #             words.remove(word)
    #     for i in range(len(words)):
    #         words[i] = wordnet_lemmatizer.lemmatize(words[i], self.get_wordnet_pos(words[i]))
    #     return ' '.join(words)


    # def bulk_lemmatize(self, column_to_clean='readme'):
    #     self.df[column_to_clean] = self.df[column_to_clean].apply(lemmatize)



    def preprocess(self):
        print('preprocessing data...')
        try:
            self.bulk_delete_code_blocks() # delete code blocks
            self.bulk_remove_markdown() # remove markdown
            self.remove_punctuation_and_escapes() # remove punctuations and escape characters
            self.bulk_delete_redundent_spaces() # delete redundent spaces
            self.bulk_to_lower_case() # convert to lower case
            self.write_faulty_index_to_txt_file()
            self.remove_faulty_rows()
            self.bulk_convert_purpose_to_sentence()

        except FileNotFoundError:
            logging.error(FileNotFoundError)

    def export(self):
        print('exporting...')
        if self.extractive:
            self.df.to_csv(
                f'data/cleaned_data_extractive/{self.filename}'
            )
        else:
            self.df.to_csv(
                f'data/cleaned_data/{self.filename}'
            )

    def report(self):
        print(self.faulty_indices)
        return self.faulty_indices

if __name__ == '__main__':
    train_preprocessor = Preprocessor(
        ORIGINAL_DATA_TRAIN,
        OUTPUT_FILE_TRAIN,
        extractive=True
    )
    eval_preprocessor = Preprocessor(
        ORIGINAL_DATA_VALID,
        OUTPUT_FILE_VALID,
        extractive=True
    )
    test_preprocessor = Preprocessor(
        ORIGINAL_DATA_TEST,
        OUTPUT_FILE_TEST,
        extractive=True
    )

    preprocessors = [train_preprocessor, eval_preprocessor, test_preprocessor]

    for preprocessor in preprocessors:
        preprocessor.preprocess()
        preprocessor.report()
        preprocessor.export()