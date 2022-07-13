from device import Device
from airtest.core.api import *
from utils import Utils


class Executor:
    class Visual:
        def __init__(self, device):
            self.device = device

        def connect(self):
            init_device("Android")
            connect_device(f"android:///{self.device.serial}")

        @staticmethod
        def start_app(app):
            start_app(app)

        @staticmethod
        def click(target):
            touch(Template(target, target_pos=5))

        @staticmethod
        def validate_components(views, components):
            valid_components = []
            for view in views:
                x_min, y_min, x_max, y_max = view.get_x_y()
                for component in components:
                    center_x, center_y = component.get_center()
                    if x_min < center_x < x_max and y_min < center_y < y_max and view.clickable:
                        valid_components.append(component)
            print(len(valid_components))
            return valid_components

    class Layout:
        pass


if __name__ == '__main__':
    dd = Device("emulator-5554")
    ev = Executor.Visual(dd)
    ev.connect()
    # ev.start_app("com.example.appdemo")
    # ev.click("01.png")

    hierarchy_path = os.path.join("tmp", "emulator-5554", "hierarchy.xml")
    views = Utils.get_all_views(hierarchy_path)
    output = "D:\\Project\\Testing\\UIED\\data\\output\\ip\\02.json"
    components = Utils.get_all_visual_components(output)
    print(ev.validate_components(views, components))
