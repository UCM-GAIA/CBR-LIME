import os
from random import randint
import sys
from tqdm import tqdm

from utils.lime_configuration import lime_configuration
from utils.lime_algorithm import lime_algorithm
import utils.system
import utils.images


def doWork(image_folder: str, result_folder: str, save_perturb: bool, perturb_folder: str):
    '''
    Calculate the perturbed image dataset for the experiment.

    Calculate the perturbed image dataset to use in the experiemnt, generates 
    nine perturbed images for each one in the original image dataset.

    Parameters:
    image_folder,   folder path with the image dataset.
    result_folder,  folder for the generated perturbed dataset.
    save_perturb,   save the original image perturbed.
    perturb_folder, folder to store the original image perturbed.
    '''

    _kernel_size = [(2, 5), (6, 10)]
    _disturbances = [100, 200]
    _kernel_width = [0.25, 0.75]

    utils.system.create_folder(result_folder)
    if save_perturb:
        utils.system.create_folder(perturb_folder)

    app = lime_algorithm()

    img_list = utils.system.ls(os.path.join(os.getcwd(), image_folder))
    configurations = list()

    for img in img_list:
        configurations.append(lime_configuration(img, 4, 150, 0.25))

        for i_ks in _kernel_size:
            _ksize = randint(i_ks[0], i_ks[1])
            for i_d in _disturbances:
                _disturb = i_d
                for i_kw in _kernel_width:
                    _kwidth = i_kw

                    configurations.append(lime_configuration(
                        img, _ksize, _disturb, _kwidth))

    for config in tqdm(configurations, desc='Calculate predictions: '):
        image = app.get_lime_explication(
            config, save_perturb=True, perturb_folder=perturb_folder)
        _save_image(image, config, result_folder)


def _save_image(image, config, folder):
    '''
    Store the image in disk.

    Parameters:
        image,  image object.
        config, lime configuration object. 
        folder, path to store the images
    '''

    name = ('__'.join([os.path.splitext(config.get_file_name())[0], str(config.get_kernel_size()).replace('.', '_'), str(
        config.get_disturbances()).replace('.', '_'), str(config.get_kernel_width()).replace('.', '_'), str(
        config.get_top_features()).replace('.', '_')]))+os.path.splitext(config.get_file_name())[1]

    path = os.path.join(os.path.join(os.getcwd(), folder), name)
    utils.images.saveImage(path, image)


def main(argv):
    """
    Main function.
    """

    ifolder = 'topImg'
    ofolder = 'explications'
    sperturb = False
    pfolder = 'perturb'

    doWork(ifolder, ofolder, sperturb, pfolder)
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
