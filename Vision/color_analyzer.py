import cv2 as cv
import numpy as np
import os
import contour_finder as con

def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
            print('Name: ' + filename)
    return images

def display_images(images):
    count = 1
    for img in images:
        cv.imshow('solar'+str(count), img)
        count += 1

def average_color(img):
    blue = []
    green = []
    red = []
    for i in img:
        for j in i:
            b = j[0]
            g = j[1]
            r = j[2]
            if not (b == 0 and g == 0 and r == 0):
                blue.append(b)
                green.append(g)
                red.append(r)
    blue_avg = np.round(np.average(blue))
    green_avg = np.round(np.average(green))
    red_avg = np.round(np.average(red))
    return [blue_avg, green_avg, red_avg]

def tint_images(images):
    fused_images = []
    for img in images:
        tint_img = np.full(img.shape, (141,181,217), np.uint8)
        fused_images.append(cv.addWeighted(img, 0.5, tint_img, 0.5, 0))
    return fused_images

def filter_images(images, masks):
    filtered_images = []
    count = 0
    for img in images:

        gray_images = con.grayscale_images(images)

        boxes = con.find_edges(gray_images[count], 72, 350)
        
        masks[count] = cv.fillPoly(masks[count], boxes, (255,255,255))
        
        # cv.drawContours(img, boxes, -1, (255,255,0), 3)
        filtered_images.append(cv.bitwise_and(img, masks[count]))
        count += 1
    return filtered_images
        

if __name__ == "__main__":

    images = load_images('Github/Solar-Panel-Cleaning-Robot/Pictures')
    # Tint: B-141 G-181 R-217
    
    tinted_images = tint_images(images)
    # display_images(images)
    # display_images(tinted_images)
    count = 0
    img = images[count]
    tint_img = tinted_images[count]
    print(average_color(img))
    print(average_color(tint_img))

    masks = con.mask_images(images)

    filtered_clean_images = filter_images(images, masks)
    filtered_tinted_images = filter_images(tinted_images, masks)
    
    clean_result = np.hstack((filtered_clean_images[count], img))
    tinted_result = np.hstack((filtered_tinted_images[count], tint_img))
    print(average_color(clean_result))
    print(average_color(tinted_result))
    cv.imshow('Result', np.hstack((clean_result, tinted_result)))
    cv.waitKey(0)