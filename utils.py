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

    # @staticmethod
    # def get_x_y(bounds):
    #     """
    #     Get the integers of minX, minY, maxX, maxY from the bounds string.
    #     :param bounds: The string of bounds.
    #     :return: Integers of minX, minY, maxX, maxY.
    #     """
    #     matcher = r"\[(\d*),(\d*)\]\[(\d*),(\d*)\]"
    #     res = re.search(matcher, bounds)
    #     return int(res.group(1)), int(res.group(2)), int(res.group(3)), int(res.group(4))


if __name__ == '__main__':
    # dd = Device("emulator-5554")
    # dd.connect()
    # hierarchy = dd.dump_2nd()
    # Utils.get_all_views(hierarchy)
    print(Utils.get_x_y("[0,2344][1440,2392]"))
