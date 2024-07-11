import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from ..model.model import get_model

def image_to_feature_vector(img):
    """convert an image to a feature vector using the model"""
    # resize the image to 224x224
    img = img.resize((224, 224))
    # convert the image to an array
    img_array = image.img_to_array(img)
    # expand the dimensions to match the model input
    img_array = np.expand_dims(img_array, axis=0)
    # preprocess the image array
    img_array = preprocess_input(img_array)
    model = get_model()
    # predict the features using the model
    features = model.predict(img_array)
    return features.flatten()