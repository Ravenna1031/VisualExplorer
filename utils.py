import os.path

from view import View, Component
import xml.etree.ElementTree as Et
import json


class Utils:

    @staticmethod
    def get_all_views(xml):
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
        with open(output, "r") as f:
            data = json.load(f)
        f.close()
        components = []
        for c in data["compos"]:
            if c["class"] == "Compo":
                component = Component(c)
                components.append(component)
        # print(len(components))
        return components


if __name__ == '__main__':
    output = os.path.join("example", "result.json")
    Utils.get_all_visual_components(output)
