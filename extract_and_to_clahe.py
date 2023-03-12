import time
import cv2
import numpy as np
import os


def enlightment(frame, gridSize=4, clipLimit=2, gamma=1):
    """
    Take image(BGR) returns enchanted image(BGR) using Contrast Limited Adaptive Histogram Equalization \
    (https://docs.opencv.org/3.4/d5/daf/tutorial_py_histogram_equalization.html)

    :param image: image array (BGR)
    :param gridSize: (optional) default 4
    :param clipLimit: (optional) default 2
    :param gamma: (optional) default 0.7
    :return: enchanted image (BGR)
    """
    image = frame.copy()

    # Contrast Limited Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=clipLimit,
                            tileGridSize=(gridSize, gridSize))

    # image.setflags(write=1)
    for i in range(3):
        image[:, :, i] = clahe.apply((image[:, :, i]))

    # Alternative
    if gamma == 0:
        return image

    # Build a lookup table mapping the pixel values [0, 255]
    # their adjusted gamma values
    inverted = 1.0 / gamma
    table = np.array([((i / 255.0) ** inverted) *
                     255 for i in np.arange(256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def simple():

    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture('vid (9).mp4')

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video file")

    # Read until video is completed
    while(cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        print(ret)
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # # Break the loop
        # else:
        #     break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    """
    Parent foler
        dataset
            [*.mp4]
        output
            [img_*.jpg]
        to_clahe.py
    """
    # simple()

    videos_dir = './raw_video'
    out_dir = './output'
    path_to_vid = os.listdir(f'{videos_dir}/')
    count = 0
    frame_count = 0
    file_count = 0
    # Here I construct a list of relative path strings for each image
    path_to_vid = [
        f"{videos_dir}/{file_name}" for file_name in path_to_vid]

    for file_name in path_to_vid:
        break_count = 0
        cap = cv2.VideoCapture(file_name)
        print(f' << Reading {file_name} >> ')

        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                frame = enlightment(frame)

                # cv2.imshow('frame', frame)

                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     break
                if count % 30 == 0:
                    cv2.imwrite(f"{out_dir}/img_{frame_count}.jpg", frame)
                    print(f"Writing {out_dir}/img_{frame_count}.jpg")
                    frame_count += 1
                count += 1

            else:
                break_count += 1
                if break_count > 50:

                    break

        # When everything done, release
        # the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()
