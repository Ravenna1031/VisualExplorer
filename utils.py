import os

from skimage.metrics import structural_similarity as ssim
from view import View, Component
import xml.etree.ElementTree as Et
import json
from loguru import logger
import cv2


class Utils:

    @staticmethod
    def get_all_views(xml):
        """
        Get all views(including all parents and children) from the hierarchy xml file.
        :param xml: The path of xml file.
        :return: A list with all views.
        """
        tree = Et.parse(xml)
        views = []
        for p in tree.iter():
            if p.tag == "node":
                view = View(p)
                views.append(view)
        return views

    @staticmethod
    def get_all_visual_components(output):
        """
        Get all components from the visual detection result.
        :param output: The path of the output.json file.
        :return: A list with all components.
        """
        with open(output, "r") as f:
            data = json.load(f)
        f.close()
        components = []
        for c in data["compos"]:
            if c["class"] == "Compo":
                component = Component(c)
                components.append(component)
        return components

    @staticmethod
    def compare_similarity(image_a, image_b):
        """
        Compare the similarity of two images.
        :param image_a: The path of image A.
        :param image_b: The path of image B.
        :return:
        """
        image_a = cv2.imread(image_a)
        image_b = cv2.imread(image_b)
        image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        widget_height = image_b.shape[0]
        widget_width = image_b.shape[1]
        image_a_resize = cv2.resize(image_a, (widget_width, widget_height), interpolation=cv2.INTER_LINEAR)
        # cv2.imshow("t1", image_a_resize)
        # cv2.imshow("t2", image_b)
        # cv2.waitKey(0)
        similarity = ssim(image_a_resize, image_b)
        logger.info("Similarity: " + str(similarity))
        return similarity

    @staticmethod
    def record_sequence(context, path):
        """
        Record the sequence in a json file.
        :param context: One event in the sequence.
        :param path: The path of the json file.
        :return:
        """
        path = os.path.join(path, "sequence.json")
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f_w:
                f_w.write(json.dumps([]))
            f_w.close()
        with open(path, "r", encoding="utf-8") as f_r:
            tmp = json.load(f_r)
            tmp.append(context)
            f_r.close()
            with open(path, "w", encoding="utf-8") as f_rw:
                f_rw.write(json.dumps(tmp))
        f_rw.close()

    @staticmethod
    def get_latest_view():
        """
        Get the latest view from the sequence.
        :return: The latest view.
        """
        path = os.path.join("Output", "sequence", "emulator-5554", "sequence.json")
        with open(path, "r", encoding="utf-8") as f:
            j = json.load(f)
            f.close()
            return j[-1]


if __name__ == '__main__':
    f_path = os.path.join("Output", "sequence", "emulator-5554")
    a = {
        "a": 123,
        "b": 234
    }
    print(Utils.get_latest_view())
