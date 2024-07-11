from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D

# initialize the model as a global variable
model = None

def initialize_model():
    global model
    # load the VGG16 model without the top layer
    base_model = VGG16(weights='imagenet', include_top=False)
    # create a new model that outputs global average pooling of the VGG16 output
    model = Model(inputs=base_model.input, outputs=GlobalAveragePooling2D()(base_model.output))

def get_model():
    global model
    if model is None:
        initialize_model()
    return model