import cv2 as cv
import numpy as np
import color_analyzer as color

"""
This is here as a place holder for trackbars
"""
def nothing(x):
    pass

"""
mask_images
@param: list of images
@return: list of the masks of the images
"""
def mask_images(images):
    masks = []
    for img in images:
        masks.append(np.zeros(img.shape, np.uint8))
    return masks

"""
grayscale_images
@param: list of images
@return: list of the images grayscaled
"""
def grayscale_images(images):
    gray_images = []
    for img in images:
        gray_images.append(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
        
    return gray_images

"""
find_edges
@param: the grayscale image, lower and upper threshold for edge detection
@return: the edges of the image
"""
def find_edges(gray_img, low, upper):
    edges = cv.Canny(gray_img, low, upper)
    boxes, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    return boxes

"""
threshold_finder
@param: list of images, which image to analyze
@return: NULL
"""
def threshold_finder(images, index):
    cv.namedWindow("Trackbars")
    
    cv.createTrackbar("L", "Trackbars", 72, 1028, nothing)
    cv.createTrackbar("U", "Trackbars", 350, 1028, nothing)

    gray = grayscale_images(images)
    gray = gray[index]
    img = images[index]

    while True:
        low = cv.getTrackbarPos("L", "Trackbars")
        upper = cv.getTrackbarPos("U", "Trackbars")

        mask = mask_images(images)
        mask = mask[index]

        boxes = find_edges(gray, low, upper)
        mask = cv.fillPoly(mask, boxes, (255,255,255))
        panel = cv.bitwise_and(img, mask)
        
        result = np.hstack((panel, img))
        edges = cv.Canny(gray, low, upper)
        cv.imshow('Trackbars', result)
        cv.imshow('Edges', edges)
        cv.waitKey(1)


if __name__ == "__main__":

    images = color.load_images('Github/Solar-Panel-Cleaning-Robot/Pictures')

    threshold_finder(images, 0)
    
cv.destroyAllWindows()
        