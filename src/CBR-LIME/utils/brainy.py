
import numpy as np
import sklearn.metrics
from sklearn.linear_model import LinearRegression
import keras
from keras.applications.imagenet_utils import decode_predictions
from enum import Enum, unique

import utils.images


@unique
class Model(Enum):
    MobileNet = 1
    Inception = 2


def getPredictionModel(model):
    '''
    Obtain the prediction model allowed.
    '''
    if model is Model.MobileNet:
        return keras.applications.mobilenet.MobileNet()
    if model is Model.Inception:
        return keras.applications.inception_v3.InceptionV3()


def getPrediction(model, image):
    '''
    Get the image classification.
    '''
    preds = model.predict(image[np.newaxis, :, :, :])
    return preds


def getDecodePrediction(model, image):
    '''
    Decode the classification.
    '''
    preds = getPrediction(model, image)
    dec_pred = decode_predictions(preds)
    return dec_pred[0]


def getTopPredictionClasses(model, image, number):
    '''
    Obtain the classification.
    '''
    preds = getPrediction(model, image)
    top_pred_classes = preds[0].argsort()[-number:][::-1]
    return top_pred_classes


def getDecodeTopPredictionClasses(model, image, number):
    '''
    Obtain the decoded clasification
    '''
    preds = getPrediction(model, image)
    top_pred_classes = preds[0].argsort()[-number:][::-1]
    decode = decode_predictions(preds)[0]
    return top_pred_classes, decode


def doWork(model, perturbations, Xi, superpixels, num_superpixels, kernel_width, num_top_features):
    '''
    Get the predictions for the perturbations.
    '''
    # Get the original prediction
    top_pred_classes = getTopPredictionClasses(model, Xi, 5)

    # Get the predictions
    total, actual = len(perturbations), 0

    predictions = []
    for pert in perturbations:
        perturbed_img = utils.images.perturb_image(Xi, pert, superpixels)
        pred = getPrediction(model, perturbed_img)
        predictions.append(pred)
        actual += 1
        print(str(actual)+'/'+str(total))

    predictions = np.array(predictions)
    # print(predictions.shape)

    # Distance calculation
    original_image = np.ones(num_superpixels)[np.newaxis, :]  # Original image
    distances = sklearn.metrics.pairwise_distances(
        perturbations, original_image, metric='cosine').ravel()
    # print(distances.shape)

    # Transform distance to 0..1 value
    # kernel_width = 0.25
    weights = np.sqrt(np.exp(-(distances**2)/kernel_width**2))

    # Clase con la mas prioridad predecida de la imagen original
    class_to_explain = top_pred_classes[0]
    simpler_model = LinearRegression()
    simpler_model.fit(
        X=perturbations, y=predictions[:, :, class_to_explain], sample_weight=weights)
    coeff = simpler_model.coef_[0]

    # Se obtienen los cuatro super pixeles que mas aportan a la predicción original
    # num_top_features = 4
    top_features = np.argsort(coeff)[-num_top_features:]

    # Crear una imagen solo con los super pixeles mas relevantes activados
    mask = np.zeros(num_superpixels)
    mask[top_features] = True  # Activar solo los super pixeles seleccionados

    return mask
