import numpy as np
import cv2


class Preprocess:
    """ preprocess using hsv """

    def __init__(self,bins):
        self.bins=bins

    def histogram(self, img, mask):
        # 3D histogram equalization
        hist = cv2.calcHist([img],[0, 1 ,2],mask,self.bins,[0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist,hist)
        hist = hist.flatten()
        #TODO: do equalization
        return hist

    def describe(self,image, mode=""):
        # by default convert to hsv
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # divide it to 3x3
        features = []
        # get image shape
        (h,w) = image.shape[:2]
        divx = int(w/3)
        divy = int(h/3)

        segments = [
            (0, divx, 0, divy), (divx, 2*divx, 0, divy), (2*divx, w, 0, divy),
            (0, divx, divy, divy*2), (divx, 2*divx, divy, divy*2), (2*divx, w, divy, divy*2),
            (0, divx, divy*2, h), (divx, 2*divx, divy*2, h), (2*divx, w, divy*2, h),
        ]

        # loop over segments
        for (startX, endX, startY, endY)  in segments:
            # create a mask
            mask = np.zeros(image.shape[:2], np.uint8)
            cv2.rectangle(mask, (startX, startY), (endX, endY), 255, -1)

            hist = self.histogram(image, mask)
            features.extend(hist)
        return features
