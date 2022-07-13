import re


class View:
    def __init__(self, element):
        """
        A view object in the 2nd gen layout.
        :param element: An element read from the layout xml file.
        """
        self.index = element.attrib["index"]
        self.text = element.attrib["text"]
        self.resource_id = element.attrib["resource-id"]
        self.class_name = element.attrib["class"]
        self.package = element.attrib["package"]
        self.content_desc = element.attrib["content-desc"]
        self.checkable = element.attrib["checkable"]
        self.checked = element.attrib["checked"]
        self.clickable = element.attrib["clickable"]
        self.enabled = element.attrib["enabled"]
        self.focusable = element.attrib["focusable"]
        self.focused = element.attrib["focused"]
        self.scrollable = element.attrib["scrollable"]
        self.long_clickable = element.attrib["long-clickable"]
        self.password = element.attrib["password"]
        self.selected = element.attrib["selected"]
        self.visible_to_user = element.attrib["visible-to-user"]
        self.bounds = element.attrib["bounds"]

    def get_x_y(self):
        """
        Get the integers of minX, minY, maxX, maxY from the bounds string.
        :return: Integers of minX, minY, maxX, maxY.
        """
        matcher = r"\[(\d*),(\d*)\]\[(\d*),(\d*)\]"
        res = re.search(matcher, self.bounds)
        return int(res.group(1)), int(res.group(2)), int(res.group(3)), int(res.group(4))

    def print_attributes(self):
        print("index: " + self.index)
        print("text: " + self.text)
        print("resource-id: " + self.resource_id)
        print("class: " + self.class_name)
        print("package: " + self.package)
        print("content-desc: " + self.content_desc)
        print("checkable: " + self.checkable)
        print("checked: " + self.checked)
        print("clickable: " + self.clickable)
        print("enabled: " + self.enabled)
        print("focusable: " + self.focusable)
        print("focused: " + self.focused)
        print("scrollable: " + self.scrollable)
        print("long-clickable: " + self.long_clickable)
        print("password: " + self.password)
        print("selected: " + self.selected)
        print("visible_to_user: " + self.visible_to_user)
        print("bounds: " + self.bounds)


class Component:
    def __init__(self, element):
        """
        A component object from the 3rd gen detection.
        :param element: A component read from the detection output json file.
        """
        self.id = element["id"]
        self.class_name = element["class"]
        self.column_min = element["column_min"]
        self.row_min = element["row_min"]
        self.column_max = element["column_max"]
        self.row_max = element["row_max"]
        self.width = element["width"]
        self.height = element["height"]

    def get_center(self):
        """
        Get the center coordinate of the detected component.
        :return: The center coordinate.
        """
        center_x = (self.row_min + self.row_max) / 2
        center_y = (self.column_min + self.column_max) / 2
        return center_x, center_y
