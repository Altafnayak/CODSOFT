import numpy as np
import tensorflow as tf # type: ignore
from tensorflow.keras.layers import Input, Dense, Embedding, LSTM, Dropout, Add # type: ignore
from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.applications import InceptionV3# type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences# type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer# type: ignore
from tensorflow.keras.applications.inception_v3 import preprocess_input# type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array# type: ignore

# Load the InceptionV3 model pre-trained on ImageNet
inception_model = InceptionV3(weights='imagenet')
model_new = Model(inception_model.input, inception_model.layers[-2].output)

# Function to preprocess the image
def preprocess_image(img_path):
    img = load_img(img_path, target_size=(299, 299))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# Function to encode an image into a feature vector
def encode_image(img_path):
    img = preprocess_image(img_path)
    feature_vector = model_new.predict(img)
    feature_vector = feature_vector.flatten()  # Flattening the vector to a 1D array
    return feature_vector

# Captioning model
def create_caption_model(vocab_size, max_length):
    inputs1 = Input(shape=(2048,))
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)
    
    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)
    
    decoder1 = Add()([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)
    
    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    
    return model

# Example of tokenizing and padding sequences
tokenizer = Tokenizer()
captions = ["a caption", "another caption"]  # Example captions
tokenizer.fit_on_texts(captions)
vocab_size = len(tokenizer.word_index) + 1
max_length = max(len(caption.split()) for caption in captions)

# Example image path
image_path = r("image path")

# Example encoded image
image_features = encode_image(image_path)

# Example caption sequence
caption = "a caption"
seq = tokenizer.texts_to_sequences([caption])[0]
seq = pad_sequences([seq], maxlen=max_length)

# Create and compile the model
caption_model = create_caption_model(vocab_size, max_length)

# Summary of the model
caption_model.summary()
