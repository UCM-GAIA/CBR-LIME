import getopt
from heapq import nlargest
import keras
from keras.applications.imagenet_utils import decode_predictions
import numpy as np
import os
import sys
import skimage
import skimage.segmentation
from skimage import io
from tqdm import tqdm

import utils.system
import utils.images


def doWork(inputFolder: str, outputFolder: str, selection_size: int = 200):
    '''
    Filter and select the top image predictions.

    For each image in the input folder recived obtain the top classification 
    value, select the most accurate and copy it to the output folder recived.

    inputFolder,    folder with the images
    outputFolder,   folter to copy the images
    selection_size, number of images to select
    '''
    images = utils.system.ls(os.path.join(os.getcwd(), inputFolder))
    data = list()
    model = keras.applications.mobilenet.MobileNet()

    for image in tqdm(images, desc='Calculate predictions: '):
        try:
            l_image=utils.images.loadImage(image)
            preds = model.predict(l_image[np.newaxis, :, :, :])
            prediction = decode_predictions(preds)[0]

            data.append([image, prediction[0][1], prediction[0][2]])
        except:
            # Ignore prediction errors
            pass

    topAcuracityPrediction = nlargest(selection_size, data, key=lambda e: e[2])

    utils.system.create_folder(outputFolder)

    for origin, pred, percent in tqdm(topAcuracityPrediction, desc='Copy results :'):
        destiny = os.path.join(os.path.join(os.getcwd(), outputFolder), os.path.splitext(os.path.basename(
            origin))[0]+'__'+str(pred)+'__'+str(percent)+os.path.splitext(os.path.basename(origin))[1])

        image = skimage.io.imread(origin)
        image = skimage.transform.resize(image, (224, 224))

        skimage.io.imsave(destiny, image)

    print('End work')


def main(argv):
    """
    Main function.
    """

    helpUsage = '01_filter_images.py -i <input folder>\n'\
        '  input folder -> folder with images\n'
    ifolder = 'image_dataset'
    ofolder = 'topImg'

    try:
        opts, _ = getopt.getopt(argv, "hi:", ["ifolder="])
        if len(opts) != 1:
            raise getopt.GetoptError(msg='Incorrect param number')
    except getopt.GetoptError as err:
        print(f'Error in the execution: {err.msg}')
        print(helpUsage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpUsage)
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            ifolder = arg


    doWork(ifolder, ofolder)
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
