import math

import cv2


class Image:
    def __init__(self, path):
        self.path = path
        self.image = cv2.imread(path)
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

    def crop_init(self):
        crop_start = math.floor(0.12 * self.height)
        crop_end = math.floor(0.92 * self.height)
        crop_img = self.image[crop_start:crop_end, :]
        # cv2.imshow("cropped", corp_img)
        # cv2.waitKey(0)
        pos_insert = self.path.find(".png")
        corp_path = self.path[:pos_insert] + "_cropped" + self.path[pos_insert:]
        cv2.imwrite(corp_path, crop_img)


if __name__ == '__main__':
    img_path = "D:\\Project\\Testing\\Image\\04.png"
    img = Image(img_path)
    img.crop_init()
