import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def extract_features(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        return None

    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    # Normalize the histogram
    hist = cv2.normalize(hist, hist).flatten()

    return hist
