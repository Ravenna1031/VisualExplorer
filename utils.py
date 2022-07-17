import os

from skimage.metrics import structural_similarity as ssim
from view import View, Component
import xml.etree.ElementTree as Et
import json


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
        return ssim(image_a, image_b)

    @staticmethod
    def record_sequence(context, path):
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


if __name__ == '__main__':
    f_path = os.path.join("Output", "sequence", "emulator-5554")
    a = {
        "a": 123,
        "b": 234
    }
    Utils.record_sequence(a, f_path)