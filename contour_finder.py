import cv2 as cv
import numpy as np
import plotly.express as px

def nothing():
    pass

if __name__ == "__main__":
    print("Hello")
    # Need to apply canny edge detection
    img = cv.imread('/Users/sam/Documents/solar1.jpeg',0)

    while True:
        cv.createTrackbar("L", "Trackbars", 0, 255, nothing)
        cv.createTrackbar("U", "Trackbars", 0, 255, nothing)
        edges = cv.Canny(img,150,160)
        fig = px.imshow(edges)
        fig.show()