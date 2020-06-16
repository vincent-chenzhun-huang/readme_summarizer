from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer

SUMMARIZAERS = {
    'LexRank': LexRankSummarizer,
    'Edmunson': EdmundsonSummarizer,
}

LANGUAGE = 'english'

SENTENCES_COUNT = 1


class ExtractiveSummarizer:
    def __init__(self, summarizer, sources):
        self.sum_name = summarizer
        self.sources = sources

    def summarize(self, source):
        parser = PlaintextParser.from_string(source, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = SUMMARIZAERS[self.sum_name](stemmer)

        if self.sum_name == 'Edmunson':
            summarizer.bonus_words = parser.significant_words
            summarizer.stigma_words = parser.stigma_words
            summarizer.null_words = get_stop_words(LANGUAGE)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        results = []
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            results.append(str(sentence))
        return results[0]

    def bulk_summarize(self):
        print('Bulk Summarizing...')
        self.sources.apply(self.summarize)


