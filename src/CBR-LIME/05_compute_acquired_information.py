import os
import operator
import skimage.io
import sys
from tqdm import tqdm

import utils.system
from utils.lime_configuration import lime_configuration as LimeConfiguration
from utils.lime_algorithm import lime_algorithm as LimeExplication


def _compute_acquired_information(in_folder: str, out_file: str, original_folder: str, simil_dict: str) -> str:
    '''
    Process the results of the experiment.

    Process the results generated in the LimeExperiment, generates
    a csv file with the information and returns the file path

    Parameters
        in_folder,          folder with the files generated in the Experiment
        out_file,           file path for save the data
        original_folder,    original images folder
        simil_dict,         file with the similitude dictionary representation
    '''
    simil_data, _ = utils.system.load_simil_dict_file_data(
        simil_dict)

    data = list()

    for input_file in utils.system.ls(in_folder):
        data_file = utils.system.read_csv(input_file)
        data.extend(data_file)

    aux = dict()
    for i in range(0, len(data)):
        if data[i][0] in aux:
            aux[data[i][0]].append(data[i])
        else:
            aux[data[i][0]] = [data[i]]

    data.clear()
    data = dict()

    app = LimeExplication()
    path = 'experiment_perturb'
    text_2_output = list()

    utils.system.create_folder(path)

    for k, v in tqdm(simil_data.items()):
        line = list()
        line.append(k.split('__')[0])

        nn1 = sorted(v.items(),
                     key=operator.itemgetter(1),
                     reverse=True)[:1]

        img_code = nn1[0][0].split('__')[0]
        original_code = k.split('__')[0]

        # Start 1nn
        KernelSize = 0
        Disturbances = 0
        KernelWidth = 0.0
        Features = 0
        div = len(aux[img_code])

        for elem in aux[img_code]:
            KernelSize += int(elem[3])
            Disturbances += int(elem[4])
            KernelWidth += float(elem[5].replace('_', '.'))
            Features += int(elem[6])

        KernelSize = int(KernelSize/div)
        Disturbances = int(Disturbances/div)
        KernelWidth = KernelWidth/div
        Features = int(Features/div)

        config = LimeConfiguration(os.path.join(
            original_folder, k), KernelSize, Disturbances, KernelWidth)
        config.__top_features = Features

        image = app.get_lime_explication(config, save_perturb=False)

        name = ('__'.join([original_code, '1nn', str(config.get_kernel_size()).replace('.', '_'), str(config.get_disturbances()).replace('.', '_'), str('%.2f' % config.get_kernel_width()).replace('.', '_'), str(config.get_top_features()).replace('.', '_')
                           ]))+os.path.splitext(config.get_file_name())[1]

        name = os.path.join(path, name)
        _path = os.path.join(os.getcwd(), name)

        skimage.io.imsave(_path, image)
        line.append(name)
        # End 1nn

        # Start 3nn
        KernelSize = 0
        Disturbances = 0
        KernelWidth = 0.0
        Features = 0
        div = 0

        nn3 = sorted(v.items(),
                     key=operator.itemgetter(1),
                     reverse=True)[:3]

        for nn in nn3:
            img_code = nn[0].split('__')[0]
            div += len(aux[img_code])

            for elem in aux[img_code]:
                KernelSize += int(elem[3])
                Disturbances += int(elem[4])
                KernelWidth += float(elem[5].replace('_', '.'))
                Features += int(elem[6])

        KernelSize = int(KernelSize/div)
        Disturbances = int(Disturbances/div)
        KernelWidth = KernelWidth/div
        Features = int(Features/div)

        config = LimeConfiguration(os.path.join(
            original_folder, k), KernelSize, Disturbances, KernelWidth)
        config.__top_features = Features

        image = app.get_lime_explication(config, save_perturb=False)

        name = ('__'.join([original_code, '3nn', str(config.get_kernel_size()).replace('.', '_'), str(config.get_disturbances()).replace('.', '_'), str('%.2f' % config.get_kernel_width()).replace('.', '_'), str(config.get_top_features()).replace('.', '_')
                           ]))+os.path.splitext(config.get_file_name())[1]

        name = os.path.join(path, name)
        _path = os.path.join(os.getcwd(), name)

        skimage.io.imsave(_path, image)
        line.append(name)
        # End 3nn

        # Start 5nn
        KernelSize = 0
        Disturbances = 0
        KernelWidth = 0.0
        Features = 0
        div = 0

        nn5 = sorted(v.items(),
                     key=operator.itemgetter(1),
                     reverse=True)[:5]

        for nn in nn5:
            img_code = nn[0].split('__')[0]
            div += len(aux[img_code])

            for elem in aux[img_code]:
                KernelSize += int(elem[3])
                Disturbances += int(elem[4])
                KernelWidth += float(elem[5].replace('_', '.'))
                Features += int(elem[6])

        KernelSize = int(KernelSize/div)
        Disturbances = int(Disturbances/div)
        KernelWidth = KernelWidth/div
        Features = int(Features/div)

        config = LimeConfiguration(os.path.join(
            original_folder, k), KernelSize, Disturbances, KernelWidth)
        config.__top_features = Features

        image = app.get_lime_explication(config, save_perturb=False)

        name = ('__'.join([original_code, '5nn', str(config.get_kernel_size()).replace('.', '_'), str(config.get_disturbances()).replace('.', '_'), str('%.2f' % config.get_kernel_width()).replace('.', '_'), str(config.get_top_features()).replace('.', '_')
                           ]))+os.path.splitext(config.get_file_name())[1]

        name = os.path.join(path, name)
        _path = os.path.join(os.getcwd(), name)

        skimage.io.imsave(_path, image)
        line.append(name)
        # End 5nn

        # Start 7nn
        KernelSize = 0
        Disturbances = 0
        KernelWidth = 0.0
        Features = 0
        div = 0

        nn7 = sorted(v.items(),
                     key=operator.itemgetter(1),
                     reverse=True)[:7]

        for nn in nn7:
            img_code = nn[0].split('__')[0]
            div += len(aux[img_code])

            for elem in aux[img_code]:
                KernelSize += int(elem[3])
                Disturbances += int(elem[4])
                KernelWidth += float(elem[5].replace('_', '.'))
                Features += int(elem[6])

        KernelSize = int(KernelSize/div)
        Disturbances = int(Disturbances/div)
        KernelWidth = KernelWidth/div
        Features = int(Features/div)

        config = LimeConfiguration(os.path.join(
            original_folder, k), KernelSize, Disturbances, KernelWidth)
        config.__top_features = Features

        image = app.get_lime_explication(config, save_perturb=False)

        name = ('__'.join([original_code, '7nn', str(config.get_kernel_size()).replace('.', '_'), str(config.get_disturbances()).replace('.', '_'), str('%.2f' % config.get_kernel_width()).replace('.', '_'), str(config.get_top_features()).replace('.', '_')
                           ]))+os.path.splitext(config.get_file_name())[1]

        name = os.path.join(path, name)
        _path = os.path.join(os.getcwd(), name)

        skimage.io.imsave(_path, image)
        line.append(name)
        # End 7nn

        text_2_output.append(line)

        KernelSize = 0
        Disturbances = 0
        KernelWidth = 0.0
        Features = 0
        div = 0

        img_code = k.split('__')[0]
        div += len(aux[img_code])

        for elem in aux[img_code]:
            KernelSize += int(elem[3])
            Disturbances += int(elem[4])
            KernelWidth += float(elem[5].replace('_', '.'))
            Features += int(elem[6])

        KernelSize = int(KernelSize/div)
        Disturbances = int(Disturbances/div)
        KernelWidth = KernelWidth/div
        Features = int(Features/div)

        config = LimeConfiguration(os.path.join(
            original_folder, k), KernelSize, Disturbances, KernelWidth)
        config.__top_features = Features

        image = app.get_lime_explication(config, save_perturb=False)

        name = ('__'.join([original_code, 'experiment', str(config.get_kernel_size()).replace('.', '_'), str(config.get_disturbances()).replace('.', '_'), str('%.2f' % config.get_kernel_width()).replace('.', '_'), str(config.get_top_features()).replace('.', '_')
                           ]))+os.path.splitext(config.get_file_name())[1]

        name = os.path.join(path, name)
        _path = os.path.join(os.getcwd(), name)

        skimage.io.imsave(_path, image)

    return utils.system.write_csv(text_2_output, out_file)


def main(argv):
    """
    Main function.
    """
    experiment_path = r'experiments/'
    output_path = r'output/experimentResult.csv'
    images_path = r'topImg/'
    simil_dict = r'output/similDict.csv'

    res = _compute_acquired_information(
        experiment_path, output_path, images_path, simil_dict)
    print(f'Result file {res}')
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
