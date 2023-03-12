import cv2
import numpy as np


def randomcrop(img, gt_boxes, scale=0.5):
    '''
    ### Random Crop ###
    img: image
    gt_boxes: format [[obj x1 y1 x2 y2],...]
    scale: percentage of cropped area
    '''

    # Crop image
    height, width = int(img.shape[0]*scale), int(img.shape[1]*scale)
    x = random.randint(0, img.shape[1] - int(width))
    y = random.randint(0, img.shape[0] - int(height))
    cropped = img[y:y+height, x:x+width]
    resized = cv2.resize(cropped, (img.shape[1], img.shape[0]))

    # Modify annotation
    new_boxes = []
    for box in gt_boxes:
        obj_name = box[0]
        x1 = int(box[1])
        y1 = int(box[2])
        x2 = int(box[3])
        y2 = int(box[4])
        x1, x2 = x1-x, x2-x
        y1, y2 = y1-y, y2-y
        x1, y1, x2, y2 = x1/scale, y1/scale, x2/scale, y2/scale
        if (x1 < img.shape[1] and y1 < img.shape[0]) and (x2 > 0 and y2 > 0):
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > img.shape[1]:
                x2 = img.shape[1]
            if y2 > img.shape[0]:
                y2 = img.shape[0]
            new_boxes.append([obj_name, x1, y1, x2, y2])
    return resized, new_boxes


if __name__ == '__main__':
    x1 = 0.216406
    y1 = 0.501389
    x2 = 0.216406 + 0.066146
    y2 = 0.501389
    x3 = 0.216406
    y3 = 0.501389 + 0.993519
    x4 = 0.216406 + 0.066146
    y4 = 0.501389 - 0.993519

    # 0.216406 0.501389 0.066146 0.993519
    img = cv2.imread('test.jpg')

    pts = np.array([[x1, y2], [x2, y2], [x3, y3], [x4, y4]], np.int32)
    pts
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], True, (0, 255, 255))
    cv2.imwrite('out.jpg', img)
