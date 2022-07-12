from view import View
import xml.etree.ElementTree as Et


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
