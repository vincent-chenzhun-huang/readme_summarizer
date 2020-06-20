class SummaryWriter:
    def __init__(self, root, summaries, category, model_index):
        self.root = root
        self.summaries = summaries
        self.category = category
        self.model_index = model_index

    def write_to_txt(self, summary, index):
        with open(f'{self.root}/{self.category}{self.model_index}{index}.txt', 'w+') as fn:
            fn.write(summary)

    def bulk_write_to_txt(self):
        for i, summary in enumerate(self.summaries):
            try:
                print(i)
                self.write_to_txt(summary, i)
            except:
                print(summary, i)
        print('Successfully wrote the summaries to txt files')
