import copy
import skimage
import skimage.segmentation
import numpy as np
from skimage import io
import warnings


def loadImage(path,reescalation_size=(224,224)):
    '''
    Load image and optionally reescalate it.
    '''
    # load image
    img = skimage.io.imread(path)
    # reescalate image
    img = skimage.transform.resize(img, reescalation_size)
    img = (img - 0.5)*2
    return img


def segmentImage(img, kernel_size, max_dist, ratio):
    '''
    Segment the image.
    '''
    # segment image
    superpixels = skimage.segmentation.quickshift(
        img, kernel_size=kernel_size,
        max_dist=max_dist, ratio=ratio)
    num_superpixels = np.unique(superpixels).shape[0]
    segmented = skimage.segmentation.mark_boundaries(img/2+0.5, superpixels)
    return segmented, superpixels, num_superpixels


def saveImage(path, image):
    '''
    Save image to disk.
    '''
    warnings.filterwarnings('ignore')
    skimage.io.imsave(path, image)


def perturb_image(img, perturbation, segments):
    '''
    Perturb the image.
    '''
    active_pixels = np.where(perturbation == 1)[0]
    mask = np.zeros(segments.shape)
    for active in active_pixels:
        mask[segments == active] = 1
    perturbed_image = copy.deepcopy(img)
    perturbed_image = perturbed_image*mask[:, :, np.newaxis]
    return perturbed_image


def calculatePerturbations(num_perturb, num_superpixels):
    '''
    Generate the perturbations.
    '''
    return np.random.binomial(1, 0.5, size=(num_perturb, num_superpixels))
