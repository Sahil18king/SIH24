import os
import cv2
import numpy as np
from django.conf import settings
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt

# Function to load images and labels
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

# Paths to your datasets (using Django settings for MEDIA_ROOT)
clean_images_path = os.path.join(settings.MEDIA_ROOT, 'Garbage')
dirty_images_path = os.path.join(settings.MEDIA_ROOT, 'Garbage')

# Load images and labels
clean_images, clean_labels = load_images_from_directory(clean_images_path, label=0)
dirty_images, dirty_labels = load_images_from_directory(dirty_images_path, label=1)

# Combine clean and dirty datasets
all_images = np.concatenate((clean_images, dirty_images), axis=0)
all_labels = np.concatenate((clean_labels, dirty_labels), axis=0)

# Normalize images
all_images = all_images / 255.0

# Split into training and validation sets
train_images, val_images, train_labels, val_labels = train_test_split(all_images, all_labels, test_size=0.2, random_state=42)

# Create the train_data and val_data tuples
train_data = (train_images, train_labels)
val_data = (val_images, val_labels)

# Function to load and compile the model
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

# Function to train the model
def train_model(model, train_data, val_data, epochs=10):
    history = model.fit(train_data[0], train_data[1], validation_data=val_data, epochs=epochs, batch_size=32)
    return history

# Function to preprocess image
def preprocess_image(image):
    image = cv2.resize(image, (128, 128))
    image = image / 255.0
    return image

# Function to detect garbage
def detect_garbage(model, image):
    processed_image = preprocess_image(image)
    prediction = model.predict(np.expand_dims(processed_image, axis=0))[0][0]
    return prediction

# Function to divide image into segments
def divide_image(image, grid_size=(4, 4)):
    height, width, _ = image.shape
    grid_h, grid_w = grid_size
    segment_height = height // grid_h
    segment_width = width // grid_w

    segments = []
    for i in range(grid_h):
        for j in range(grid_w):
            segment = image[i*segment_height:(i+1)*segment_height,
                            j*segment_width:(j+1)*segment_width]
            segments.append(segment)
    return segments

# Function to calculate cleanliness and dirtiness
def calculate_cleanliness_and_dirtiness(model, image):
    segments = divide_image(image)
    total_cleanliness = 0
    total_dirtiness = 0

    for segment in segments:
        garbage_value = detect_garbage(model, segment)
        total_dirtiness += garbage_value
        total_cleanliness += (1 - garbage_value)

    num_segments = len(segments)
    average_cleanliness = total_cleanliness / num_segments
    average_dirtiness = total_dirtiness / num_segments

    return average_cleanliness, average_dirtiness

# Function to generate graph
def generate_graph(average_cleanliness, average_dirtiness):
    labels = ['Cleanliness', 'Dirtiness']
    values = [average_cleanliness, average_dirtiness]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Cleanliness vs Dirtiness')
    plt.xlabel('Metric')
    plt.ylabel('Average Value')

    plt.savefig('cleanliness_dirtiness_graph.png')
    plt.show()
