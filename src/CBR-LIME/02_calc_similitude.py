import math
import operator
import os
import sys
from tqdm import tqdm

import utils.brainy
import utils.system


def doWork(imagesPath: str):
    '''
    Calculate the similitude between images in the dataset.

    Calculate the similitude comparing the neural net classification and 
    generate two csv files one with all the dataset images and other 
    with the top 3 related images for each one.

    Parameters:
    imagesPath, folder path with the image dataset.
    '''

    images = utils.system.ls(imagesPath)

    matrix = list()
    dictionary = dict()
    clasification = dict()

    for i in range(len(images)):
        matrix.append(list())
        for _ in range(len(images)):
            matrix[i].append(None)

    # Select model
    model = utils.brainy.getPredictionModel(utils.brainy.Model.MobileNet)

    for img_path in tqdm(images, desc='Classification images '):
        img = utils.images.loadImage(img_path)

        classif = utils.brainy.getDecodePrediction(model, img)

        clasification[img_path] = classif

    for i, orig in tqdm(enumerate(images), desc='Compare similarity '):
        dictionary[orig] = dict()

        class_origin = clasification[orig]

        for j, dest in enumerate(images):
            if i != j:
                simil = _get_similarity(class_origin, clasification[dest])

                matrix[i][j] = simil
                dictionary[orig][dest] = simil

    _save_matrix(matrix, images)
    _save_top_simil_dict(dictionary, 3)

    print('Finish process :)')


def _get_similarity(class1: list, class2: list):
    '''
    Calculate the similarity between two images classification class.
    '''
    result = 0.0
    data1 = list()

    data1.extend(class1)
    data1.extend(class2)

    data2 = dict()
    for element in data1:
        if element[1] in data2:
            data2[element[1]] += element[2]
        else:
            data2[element[1]] = element[2]

    for v in data2.values():
        result += v*v

    return math.sqrt(result)


def _save_matrix(matrix: list, images: list):
    """
    Save the similitude matrix.

    Create if no exists the /output directory and save the similitude data
    between images.

    matrix, data
    """
    outputFolder = 'output'

    utils.system.create_folder(outputFolder)

    filePath = os.path.join(
        os.getcwd(), os.path.join(outputFolder, 'similMatrix.csv'))

    images.insert(0, 'Images')
    images.append('\n')
    cabecera = ';'.join(images)

    with open(filePath, 'w') as the_file:
        the_file.write(cabecera)

        for i in tqdm(range(len(matrix)), desc='Saving matrix'):
            line = list()
            line.append(str(images[i+1]))
            for value in matrix[i]:
                line.append(str(value))
            line.append('\n')

            line = ';'.join(line)
            the_file.write(line)


def _save_top_simil_dict(dictionary: dict, size: int):
    """
    Save the similitude dictionary.

    Create if no exists the /output directory and save the similitude data
    between images selecting the top number images related.

    dictionary, data
    size,        number of selected items to store
    """
    outputFolder = 'output'

    utils.system.create_folder(outputFolder)

    filePath = os.path.join(
        os.getcwd(), os.path.join(outputFolder, 'similDict.csv'))

    with open(filePath, 'w') as the_file:
        for k, v in tqdm(dictionary.items(),desc='Saving dictionary'):
            line = str(k) + ';'

            comparator = {kp: vp for kp, vp in v.items()}
            comparator = sorted(comparator.items(),
                                key=operator.itemgetter(1),
                                reverse=True)[:size]

            for i in range(len(comparator)):
                line += str(comparator[i][0]) + ';' + \
                    str(comparator[i][1]) + ';'

            the_file.write(line+'\n')


def main(argv):
    """
    Main function.
    """
    ifolder = 'topImg'
    doWork(ifolder)
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
