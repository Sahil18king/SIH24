import os
import cv2
import numpy as np
from django.conf import settings
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def load_images_from_directory(directory, label, image_size=(128, 128)):
    images = []
    labels = []
    for filename in os.listdir(directory):
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, image_size)
            images.append(img)
            labels.append(label)
    return np.array(images), np.array(labels)

# Load datasets
clean_images_path = os.path.join(settings.MEDIA_ROOT, 'Garbage', 'Clean')
dirty_images_path = os.path.join(settings.MEDIA_ROOT, 'Garbage', 'Dirty')

clean_images, clean_labels = load_images_from_directory(clean_images_path, label=0)
dirty_images, dirty_labels = load_images_from_directory(dirty_images_path, label=1)

all_images = np.concatenate((clean_images, dirty_images), axis=0)
all_labels = np.concatenate((clean_labels, dirty_labels), axis=0)

all_images = all_images / 255.0

train_images, val_images, train_labels, val_labels = train_test_split(
    all_images, all_labels, test_size=0.2, random_state=42
)

def load_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(model, train_data, val_data, epochs=10):
    history = model.fit(train_data[0], train_data[1], validation_data=val_data, epochs=epochs, batch_size=32)
    return history

if __name__ == "__main__":
    model = load_model()
    history = train_model(model, (train_images, train_labels), (val_images, val_labels), epochs=10)
    model.save('cleanliness_model.h5')
