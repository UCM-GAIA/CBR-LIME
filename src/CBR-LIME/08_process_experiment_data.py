from tqdm import tqdm

import utils.system


def _process_experiments_data(in_folder: str, out_file: str, original_folder: str, simil_dict: str) -> str:
    '''
    Process the results of the experiments.

    Process the results generated in the check hypothesis experiment and 
    generates a csv file with the information and returns the file path.

    Parameters
        in_folder,          folder with the files generated in the Lime Experiment
        out_file,           file path for save the data
        original_folder,    original images folder
        simil_dict,         file with the similitude dictionary representation
    '''

    data = list()
    aux = dict()
    result = list()
    header = list()

    for input_file in utils.system.ls(in_folder):
        data_file = utils.system.read_csv(input_file)
        data.extend(data_file)

    for i in range(0, len(data)):
        if data[i][0] in aux:
            aux[data[i][0]].append(data[i])
        else:
            aux[data[i][0]] = [data[i]]

    header = ['ID image', '# 3nn', '# Default']

    for k, v in tqdm(aux.items()):
        num_3nn = 0
        num_default = 0
        line = list()

        num_3nn = len(list(filter(lambda x: x[1] == '3nn', v)))
        num_default = len(v)-num_3nn

        line.append(k)
        line.append(num_3nn)
        line.append(num_default)

        result.append(line)

    return utils.system.write_csv(data=result, out_file=out_file, header=True, header_data=header)


def main():
    experiment_path = r'experiments2/'
    output_path = r'output/experimentResult2.csv'
    images_path = r'topImg/'
    simil_dict: str = r'output/similDict.csv'

    _process_experiments_data(
        experiment_path, output_path, images_path, simil_dict)


if __name__ == "__main__":
    main()
