import cv2 as cv
import numpy as np
import os
import contour_finder as con

"""
load_images
@param: folder (string)
@return: list of images in folder
"""
def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
            print('Name: ' + filename)
    return images

"""
display_images
@param: list of images
@return: NULL
"""
def display_images(images):
    count = 1
    for img in images:
        cv.imshow('solar'+str(count), img)
        count += 1

"""
average_color
@param: image
@return: list of the average blue, green, and red colors
"""
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

"""
tint_images
@param: images
@return: images
"""
def tint_images(images):
    fused_images = []
    for img in images:
        tint_img = np.full(img.shape, (141,181,217), np.uint8)
        fused_images.append(cv.addWeighted(img, 0.5, tint_img, 0.5, 0))
    return fused_images

"""
filter_images
@param: images, masks
@return: images with masks applied
"""
def filter_images(images: list, masks):
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

def panel_is_dirty(new_img: str) -> bool:
    # TODO: Make sure that the path is correct
    clean_image = cv.imread(os.path.join('../Pictures/', 'clean.jpg'))

    # Find out how to take a picture and store it here
    dirty_image = cv.imread(os.path.join('../Pictures/', new_img))

    # Find the masks of the images based on the clean image
    mask = con.mask_images(clean_image)

    filtered_images = filter_images([clean_image, dirty_image], mask)
    clean_color_avg = average_color(filtered_images[0])
    dirty_color_avg = average_color(filtered_images[1])

    if (dirty_color_avg[1] - 30 > clean_color_avg[1]) and (dirty_color_avg[2] - 30 > clean_color_avg[2]):
        return True
    
    return False

if __name__ == "__main__":

    images = load_images('../Pictures/')
    
    # Tint: B-141 G-181 R-217
    tinted_images = tint_images(images)

    # Specify Image to Show
    count = 2
    img = images[count]
    tint_img = tinted_images[count]

    # Display Before Mask Information
    print("Average Color Before Masks (B, G, R)")
    print("Clean:")
    print(average_color(img))
    print("Dirty:")
    print(average_color(tint_img))

    # Find the masks of the images based on the clean image
    masks = con.mask_images(images)

    # Apply the masks to both sets of images
    filtered_clean_images = filter_images(images, masks)
    filtered_tinted_images = filter_images(tinted_images, masks)
    
    # Find new average colors
    clean_result = np.hstack((img, tint_img))
    tinted_result = np.hstack((filtered_clean_images[count], filtered_tinted_images[count]))
    
    # Display After Mask Information
    print("\nAverage Color After Masks (B, G, R)")
    print("Clean: ")
    print(average_color(filtered_clean_images[count]))
    print("Dirty: ")
    print(average_color(filtered_tinted_images[count]))

    # Display Selected Image
    cv.imshow('Result', np.hstack((clean_result, tinted_result)))
    cv.waitKey(0)
    os.chdir('../Filtered Pictures')
    count = 1
    for i in filtered_clean_images:
        cv.imwrite('Filtered_Clean_' + str(count) + '.jpg', i)
        count += 1
    count = 1
    for i in filtered_tinted_images:
        cv.imwrite('Filtered_Tinted_' + str(count) + '.jpg', i)
        count += 1