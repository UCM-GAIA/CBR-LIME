import skimage.io
from skimage.metrics import structural_similarity
import sys
from tqdm import tqdm

import utils.system


def compare_neighborhood(original_images: str, experiments_images: str, explication_images: str, out_file: str):
    '''
    Generates the similarty comparation.

    Generate the similarity matrix between images and neighborhood.
    
    Parameters
        original_images,    folder path with the original image dataset
        experiments_images, folder path with the perturbed images used in the experiment
        explication_images, folder path with the explication images 
        out_file,           file path with the results
    '''

    o_images = utils.system.ls(original_images)
    e_images = utils.system.ls(experiments_images)
    expli_images = utils.system.ls(explication_images)

    text_2_output = list()

    text_2_output.append(['ID', 'Name experiment media', 'Name 1nn', 'SSIM 1nn',
                          'Name 3nn', 'SSIM 3nn', 'Name 5nn', 'SSIM 5nn',
                          'Name 7nn', 'SSIM 7nn', 'Name Default', 'SSIM Default'])

    for o_img in tqdm(o_images):
        key_original = utils.system._clean_filename(o_img).split('__')[0]

        e_filtered = list(filter(lambda x: utils.system._clean_filename(
            x).startswith(key_original + '__') == True, e_images))

        filtered = list(filter(lambda x: utils.system._clean_filename(
            x).startswith(key_original + '__') == True, expli_images))

        expli_filtered = list(filter(lambda x: x.find(
            '__4__150__0_25__14') != -1, filtered))

        name_1nn = list(filter(lambda x: x.find(
            '__1nn__') != -1, e_filtered))[0]
        name_3nn = list(filter(lambda x: x.find(
            '__3nn__') != -1, e_filtered))[0]
        name_5nn = list(filter(lambda x: x.find(
            '__5nn__') != -1, e_filtered))[0]
        name_7nn = list(filter(lambda x: x.find(
            '__7nn__') != -1, e_filtered))[0]
        name_media = list(filter(lambda x: x.find(
            '__experiment__') != -1, e_filtered))[0]

        name_Default = expli_filtered[0]

        media = skimage.io.imread(name_media)

        ssim_1nn = structural_similarity(media, skimage.io.imread(
            name_1nn), full=False, multichannel=True)
        ssim_3nn = structural_similarity(media, skimage.io.imread(
            name_3nn), full=False, multichannel=True)
        ssim_5nn = structural_similarity(media, skimage.io.imread(
            name_5nn), full=False, multichannel=True)
        ssim_7nn = structural_similarity(media, skimage.io.imread(
            name_7nn), full=False, multichannel=True)
        ssim_Default = structural_similarity(media, skimage.io.imread(
            name_Default), full=False, multichannel=True)

        text_2_output.append([key_original, name_media, name_1nn,
                              ssim_1nn, name_3nn, ssim_3nn, name_5nn,
                              ssim_5nn, name_7nn, ssim_7nn, name_Default, ssim_Default])

    utils.system.write_csv(text_2_output, out_file)


def main(argv):
    """
    Main function.
    """

    original_images = r'topImg/'
    experiments_images = r'experiment_perturb/'
    explication_images = r'explications/'
    out_file = r'output/experimentComparationResults.csv'

    compare_neighborhood(original_images, experiments_images,
                         explication_images, out_file)
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
