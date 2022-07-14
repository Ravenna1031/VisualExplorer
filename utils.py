import os.path

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
                # view.print_attributes()
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
