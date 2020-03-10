import copy
import keras
from keras.applications.imagenet_utils import decode_predictions
import numpy as np
import os
import skimage.io
from sklearn.linear_model import LinearRegression
import skimage.segmentation
import sklearn.metrics

import utils.system

class lime_algorithm():
    '''
    Apply the Lime algorithm.
    '''

    __model = 0

    def __init__(self):
        '''
        Constructor of the class.
        '''

        self.__model = keras.applications.mobilenet.MobileNet()

    def get_lime_explication(self, config, save_perturb: bool = False, perturb_folder:str=None):
        '''
        Apply the  disturbance to the image and obtain the explication.

        Parameters:
            config,         lime configuration object to disturb the image.
            save_perturb,   allow save the image perturbed
            perturb_folder, path to the image perturbed storage

        Returns:
            The image perturbed
        '''

        img = skimage.io.imread(config.get_file_path())
        if img.shape != (224, 224, 3):
            img = skimage.transform.resize(img, (224, 224))

        # Obtain 5 prediction class
        preds = self.__model.predict(img[np.newaxis, :, :, :])
        # Select top prediction
        class_to_explain = preds[0].argsort()[0]

        # Segment the image
        superpixels = skimage.segmentation.quickshift(
            img, kernel_size=config.get_kernel_size(), max_dist=200, ratio=0.2)
        num_superpixels = np.unique(superpixels).shape[0]

        # Option to save the segmented image
        if save_perturb:
            utils.system.create_folder(perturb_folder)
            skimage.io.imsave(os.path.join(perturb_folder, os.path.splitext(config.get_file_name())[0]+'_pert_'+str(config.get_kernel_size())+os.path.splitext(
                config.get_file_name())[1]), skimage.segmentation.mark_boundaries((img/2+0.5)/128, superpixels))

        # Create all perturbation
        perturbations = np.random.binomial(1, 0.5, size=(
            config.get_disturbances(), num_superpixels))

        # Create all perturbed images
        predictions = []
        for pert in perturbations:
            perturbed_img = self._perturb_image(img, pert, superpixels)
            pred = self.__model.predict(perturbed_img[np.newaxis, :, :, :])
            predictions.append(pred)

        predictions = np.array(predictions)

        original_image = np.ones(num_superpixels)[np.newaxis, :]
        distances = sklearn.metrics.pairwise_distances(
            perturbations, original_image, metric='cosine').ravel()

        # Calculate the most representative perturbations
        weights = np.sqrt(np.exp(-(distances**2)/config.get_kernel_width()**2))
        simpler_model = LinearRegression()
        simpler_model.fit(
            X=perturbations, y=predictions[:, :, class_to_explain], sample_weight=weights)
        coeff = simpler_model.coef_[0]

        # Select and create the top features image
        top_features = np.argsort(coeff)[-config.get_top_features():]

        mask = np.zeros(num_superpixels)
        mask[top_features] = True

        return self._perturb_image(img/2+0.5, mask, superpixels)

    def _perturb_image(self, img, perturbation, segments):
        '''
        Perturb the image.

        Parameters:
            img,            image object
            perturbation,   disturbance to apply to the image
            segments,       segments to perturb the image

        Returns:
            The image perturbed.
        '''

        active_pixels = np.where(perturbation == 1)[0]
        mask = np.zeros(segments.shape)

        for active in active_pixels:
            mask[segments == active] = 1

        perturbed_image = copy.deepcopy(img)
        perturbed_image = perturbed_image*mask[:, :, np.newaxis]
        return perturbed_image
