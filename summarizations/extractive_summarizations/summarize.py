from summarizations.extractive_summarizations.data_reader import DataReader
from summarizations.extractive_summarizations.extractive_summarizer import ExtractiveSummarizer
from summarizations.extractive_summarizations.extractive_summarizer import SUMMARIZAERS
from summarizations.extractive_summarizations.extractive_summarizer import LANGUAGE
from summarizations.extractive_summarizations.extractive_summarizer import SENTENCES_COUNT

if __name__ == '__main__':
    data_reader = DataReader(
        '/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/cleaned_data_extractive/test.cleaned_readme_data.csv')
    test_df = data_reader.read()
    lex_rank = ExtractiveSummarizer('LexRank', test_df['readme'])
    edmunson = ExtractiveSummarizer('Edmunson', test_df['readme'])
    lead_cm = ExtractiveSummarizer('LeadCM', test_df['readme'])

    lex_rank_summarizations = lex_rank.bulk_summarize()
    edmunson_summarizations = edmunson.bulk_summarize()
    lead_cm_summarizations = lead_cm.bulk_summarize()

    test_df['lex_rank'] = lex_rank.sources
    test_df['edmunson'] = edmunson.sources
    test_df['lead_cm'] = lead_cm.sources

    test_df = test_df.drop('Unnamed: 0', 1)
    test_df.to_csv('/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/extractive_summarizations/extractive_summarizations.csv')