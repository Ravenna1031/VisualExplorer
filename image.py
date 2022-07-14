import math
import time
import cv2


class Image:
    def __init__(self, path):
        """
        An image capture from the device to detect elements.
        :param path: The path of the image.
        """
        self.path = path
        self.image = cv2.imread(path)
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

    def crop_init(self):
        """
        Crop the top(status bar) and bottom(home button, etc.) of the image.
        :return: None
        """
        crop_start = math.floor(0.12 * self.height)
        crop_end = math.floor(0.92 * self.height)
        crop_img = self.image[crop_start:crop_end, :]
        corp_path = self.image_name_insert(self.path, "_cropped")
        cv2.imwrite(corp_path, crop_img)

    def crop_component(self, image, component):
        """
        Crop the image with the bounds of the input component.
        :param image: The image to crop.
        :param component: A randomly selected component to execute.
        :return: The path of the cropped component image.
        """
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
        """
        Insert a text in the original image name.
        :param image: The path of the image.
        :param text: Text to insert.
        :return: The path of the inserted image.
        """
        assert image.endswith(".png") or image.endswith(".jpg"), "Not valid image format."
        if image.endswith(".png"):
            pos_insert = image.find(".png")
        else:
            pos_insert = image.find(".jpg")
        return image[:pos_insert] + str(text) + image[pos_insert:]
