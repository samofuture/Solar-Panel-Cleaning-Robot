import cv2 as cv
import numpy as np
# import plotly.express as px

def nothing(x):
    pass

if __name__ == "__main__":
    cv.namedWindow("Trackbars")
    
    cv.createTrackbar("L", "Trackbars", 0, 255, nothing)
    cv.createTrackbar("U", "Trackbars", 255, 255, nothing)

    img = cv.imread('/Users/sam/Documents/solar1.jpeg',0)

    while True:
        
        low = cv.getTrackbarPos("L", "Trackbars")
        upper = cv.getTrackbarPos("U", "Trackbars")

        edges = cv.Canny(img, low, upper)
        fig = np.hstack((edges,img))
        cv.imshow('Trackbars', fig)

        # If the user presses ESC then exit the program
        key = cv.waitKey(1)
        if key == 27:
            break
        
        