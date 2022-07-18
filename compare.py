import os.path
import sys

import cv2
import pyautogui
import numpy as np
from PyQt5 import QtGui

from skimage.metrics import structural_similarity as compare_ssim

class CompareImage:

    def __init__(self, base_point, image_size, image_interval):
        self.base_point = base_point
        self.image_size = image_size
        self.image_interval = image_interval
    #     self.__temp_image_save_path = os.getcwd() + '/temp'
    #     self.__create_folder(self.__temp_image_save_path)
    #
    # def __create_folder(self, path):
    #     try:
    #         if not os.path.exists(path):
    #             os.mkdir(path)
    #     except OSError:
    #         print('error : create directory fail')

    def __cv2_image_to_qIamge(self, cv2_image):
        # 참고 : https://stackoverflow.com/questions/42570214/displaying-image-using-a-label
        # 참고2 : https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
        height, width, channels = cv2_image.shape
        bytes_per_line = channels * width
        return QtGui.QImage(cv2_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()


    def set_base_position(self, base_point):
        self.base_point = base_point

    def set_image_size(self, image_size):
        self.image_size = image_size

    def set_image_interval(self, image_interval):
        self.image_interval = image_interval

    # 참고 : https://blog.naver.com/youseok0/221571933041
    # 참고2 : https://choiseokwon.tistory.com/219
    def compare(self, image1, image2):

        image_result = image2.copy()

        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        try:
            (score, diff) = compare_ssim(gray1, gray2, full=True)
            diff = (diff * 255).astype("uint8")

            thresh = cv2.threshold(diff, 0, 255,
                                   cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # 차이점 빨간색으로 칠하기
            image_result[thresh == 255] = [0, 0, 255]
        except:
            print('exception')

        # cv2 -> qt 로 보여줄 수 있는 이미지로 변환

        return self.__cv2_image_to_qIamge(image_result)
        # cv2.imshow('result!', image_result)
        # cv2.waitKey(0)

    def compare_with_path(self, image1_path, image2_path):
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        return self.compare(image1, image2)

    def crop_image_and_compare(self):
        pos = (self.base_point[0], self.base_point[1], self.image_size[0], self.image_size[1])
        image1 = self.crop_image(pos)

        pos = (self.base_point[0] + self.image_size[0] + self.image_interval, self.base_point[1], self.image_size[0], self.image_size[1])
        image2 = self.crop_image(pos)

        return self.compare(image1, image2)

    def crop_image(self, pos):
        # 참고 : https://stackoverflow.com/questions/35958071/using-pyautogui-and-opencv-for-screenshot
        img = pyautogui.screenshot(region=pos)
        open_cv_image = np.array(img)
        # Convert RGB to BGR
        return open_cv_image[:, :, ::-1].copy()

