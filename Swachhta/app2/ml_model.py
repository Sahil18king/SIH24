import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model


base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, 'cleanliness_model.h5')
model = load_model(model_path)

def preprocess_image(image):
    image = cv2.resize(image, (128, 128))
    image = image / 255.0
    return image

def detect_garbage(model, image):
    processed_image = preprocess_image(image)
    prediction = model.predict(np.expand_dims(processed_image, axis=0))[0][0]
    return prediction

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

def generate_graph(average_cleanliness, average_dirtiness):
    labels = ['Cleanliness', 'Dirtiness']
    values = [average_cleanliness, average_dirtiness]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Cleanliness vs Dirtiness')
    plt.xlabel('Metric')
    plt.ylabel('Average Value')

    plt.savefig('media/cleanliness_dirtiness_graph.png')
