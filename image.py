import math
import time
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
        corp_path = self.image_name_insert(self.path, "_cropped")
        cv2.imwrite(corp_path, crop_img)

    def crop_component(self, image, component):
        x_min = component.column_min
        x_max = component.column_max
        y_min = component.row_min
        y_max = component.row_max
        cropped_img = cv2.imread(image)
        component_img = cropped_img[y_min:y_max, x_min:x_max]
        component_img_height = component_img.shape[0]
        component_img_width = component_img.shape[1]
        component_img = cv2.resize(component_img, (int(component_img_width * 2.54), int(component_img_height * 2.54)),
                                   interpolation=cv2.INTER_LINEAR)
        component_path = self.image_name_insert(image, int(time.time()))
        cv2.imwrite(component_path, component_img)
        return component_path

    @staticmethod
    def image_name_insert(image, text):
        assert image.endswith(".png") or image.endswith(".jpg"), "Not valid image format."
        if image.endswith(".png"):
            pos_insert = image.find(".png")
        else:
            pos_insert = image.find(".jpg")
        return image[:pos_insert] + str(text) + image[pos_insert:]


if __name__ == '__main__':
    img_path = "D:\\Project\\Testing\\Image\\05.png"
    img = Image(img_path)
    img.crop_init()
