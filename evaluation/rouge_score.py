from pyrouge import Rouge155


class RougeEvaluator:
    def __init__(self, system_dir, model_dir, system_filename_pattern, model_filename_pattern, output_path, file_name):
        self.r = Rouge155()
        self.r.system_dir = system_dir
        self.r.model_dir = model_dir
        self.r.system_filename_pattern = system_filename_pattern
        self.r.model_filename_pattern = model_filename_pattern
        self.output_path = output_path
        self.file_name = file_name

    def evaluate(self):
        output = self.r.convert_and_evaluate()
        output_dict = self.r.output_to_dict(output)
        return output, output_dict

    def write_to_txt(self):
        with open(f'{self.output_path}/{self.file_name}', 'w+') as fn:
            print('writing to txt...')
            output, output_dir = self.evaluate()
            print(output)
            print(output_dir)
            print(output_dir)
            fn.write(output)
            print(f'Check the output in {self.output_path}/{self.file_name}')
