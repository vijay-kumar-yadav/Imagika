# Import the library
import os
import cv2
import time


def convertImg(Path):
    # Read in the image
    img = cv2.imread(Path)
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_gray_image = cv2.bitwise_not(gray_image)

    # blur the image by gaussian function
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)

    # Invert the image
    inverted_blurred_image = cv2.bitwise_not(blurred_image)

    # create the pencil sketch
    pencil_sketch_img = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

    # download cache pencil image
    if os.path.exists("History") == False:
        os.mkdir("History")
        # time.time()-> time stamp ---->it generate epoch or Unix time
    getPath = "History/pencil_" + str(int(time.time())) + ".jpg"
    cv2.imwrite(getPath, pencil_sketch_img)

    return getPath
