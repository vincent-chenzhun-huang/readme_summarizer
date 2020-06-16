from evaluation.config import SYS_ROOT_DIR, MOD_ROOT_DIR, OUTPUT_PATH
from evaluation.rouge_score import RougeEvaluator
from evaluation.summary_writer import SummaryWriter
from summarizations.extractive_summarizations.data_reader import DataReader


def read_data():
    data_reader = DataReader(
        '/Users/vincenthuang/Development/Summer-2020/readme_summarizer/data/extractive_summarizations/extractive_summarizations.csv')
    readme_df = data_reader.read()
    return readme_df


def write_to_dir(readme_df):
    system_summaries = readme_df['summary'].to_list()
    lex_rank_summaries = readme_df['lex_rank'].to_list()
    edmunson_summaries = readme_df['edmunson'].to_list()

    sys_writer = SummaryWriter(SYS_ROOT_DIR, system_summaries, 'system.', '')
    lex_rank_writer = SummaryWriter(MOD_ROOT_DIR, lex_rank_summaries, 'model.', 'A.')
    edmunson_writer = SummaryWriter(MOD_ROOT_DIR, edmunson_summaries, 'model.', 'B.')

    writers = [sys_writer, lex_rank_writer, edmunson_writer]

    for writer in writers:
        writer.bulk_write_to_txt()


def calculate():
    lex_rank_evaluator = RougeEvaluator(
        SYS_ROOT_DIR,
        MOD_ROOT_DIR,
        'system.(\d+).txt',
        'model.A.#ID#.txt',
        OUTPUT_PATH,
        'lex_rank_rouge.txt'
    )
    edmunson_evaluator = RougeEvaluator(
        SYS_ROOT_DIR,
        MOD_ROOT_DIR,
        'system.(\d+).txt',
        'model.B.#ID#.txt',
        OUTPUT_PATH,
        'edmunson_rouge.txt'
    )
    evaluators = [lex_rank_evaluator, edmunson_evaluator]

    for evaluator in evaluators:
        evaluator.evaluate()
        evaluator.write_to_txt()


if __name__ == '__main__':
    readme_df = read_data()
    write_to_dir(readme_df)
    calculate()
