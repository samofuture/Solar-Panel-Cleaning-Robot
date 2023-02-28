import cv2 as cv
import numpy as np
import color_analyzer as color

def nothing(x):
    pass

def mask_images(images):
    masks = []
    for img in images:
        masks.append(np.zeros(img.shape, np.uint8))
    return masks

def grayscale_images(images):
    gray_images = []
    for img in images:
        gray_images.append(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
        
    return gray_images

def find_edges(gray_img, low, upper):
    edges = cv.Canny(gray_img, low, upper)
    boxes, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    return boxes

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
    
    masks = mask_images(images)
    gray_images = grayscale_images(images)
    
    low = 72
    upper = 350
        
    while True:
        
        count = 0
        for img in images:
            boxes = find_edges(gray_images[count], low, upper)
            
            masks[count] = cv.fillPoly(masks[count], boxes, (255,255,255))
            
            # cv.drawContours(img, boxes, -1, (255,255,0), 3)
            panel = cv.bitwise_and(img, masks[count])
            
            result = np.hstack((panel, img))
            
            if count == 0:
                cv.imshow('Trackbars', result)
            else:
                cv.imshow('solar'+str(count+1), result)
            count += 1

        # If the user presses ESC then exit the program
        key = cv.waitKey(0)
        if key == 27:
            break
cv.destroyAllWindows()
        