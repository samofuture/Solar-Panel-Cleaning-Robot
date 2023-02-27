import cv2 as cv
import numpy as np

def nothing(x):
    pass

if __name__ == "__main__":
    cv.namedWindow("Trackbars")
    
    cv.createTrackbar("L", "Trackbars", 172, 1028, nothing)
    cv.createTrackbar("U", "Trackbars", 759, 1028, nothing)

    img = cv.imread('Github/Solar-Panel-Cleaning-Robot/Pictures/solar1.jpeg')
    img2 = cv.imread('Github/Solar-Panel-Cleaning-Robot/Pictures/solar2.jpeg')
    img3 = cv.imread('Github/Solar-Panel-Cleaning-Robot/Pictures/solar3.jpeg')
    img4 = cv.imread('Github/Solar-Panel-Cleaning-Robot/Pictures/solar4.jpeg')
    
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    img3_gray = cv.cvtColor(img3, cv.COLOR_BGR2GRAY)
    img4_gray = cv.cvtColor(img4, cv.COLOR_BGR2GRAY)

    mask = np.zeros(img.shape, np.uint8)
    mask2 = np.zeros(img2.shape, np.uint8)
    mask3 = np.zeros(img3.shape, np.uint8)
    mask4 = np.zeros(img4.shape, np.uint8)

    while True:
        
        low = cv.getTrackbarPos("L", "Trackbars")
        upper = cv.getTrackbarPos("U", "Trackbars")

        edges = cv.Canny(img_gray, low, upper)
        edges2 = cv.Canny(img2_gray, low, upper)
        edges3 = cv.Canny(img3_gray, low, upper)
        edges4 = cv.Canny(img4_gray, low, upper)

        boxes, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        boxes2, _ = cv.findContours(edges2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        boxes3, _ = cv.findContours(edges3, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        boxes4, _ = cv.findContours(edges4, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # cv.drawContours(img3, boxes, -1, (255,255,0), 3)

        cv.fillPoly(mask, boxes, (255,255,255))
        cv.fillPoly(mask2, boxes2, (255,255,255))
        cv.fillPoly(mask3, boxes3, (255,255,255))
        cv.fillPoly(mask4, boxes4, (255,255,255))

        result = np.hstack((cv.bitwise_and(img, mask), img))
        result2 = np.hstack((cv.bitwise_and(img2, mask2), img2))
        result3 = np.hstack((cv.bitwise_and(img3, mask3), img3))
        result4 = np.hstack((cv.bitwise_and(img4, mask4),img4))

        cv.imshow('Trackbars', result3)
        
        cv.imshow('First', result)
        cv.imshow('Second', result2)
        cv.imshow('Fourth', result4)

        # If the user presses ESC then exit the program
        key = cv.waitKey(1)
        if key == 27:
            break
cv.destroyAllWindows()
        