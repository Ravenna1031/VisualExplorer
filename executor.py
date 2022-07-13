import random

from device import Device
from airtest.core.api import *
from utils import Utils
from image import Image


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
        def random_select_component(output):
            components = Utils.get_all_visual_components(output)
            return random.choice(components)

    class Layout:
        pass


if __name__ == '__main__':
    dd = Device("emulator-5554")
    ev = Executor.Visual(dd)
    ev.connect()
    output = os.path.join("example", "result.json")
    component = ev.random_select_component(output)
    img_path = os.path.join("example", "result.jpg")
    img = Image(img_path)
    compo = img.crop_component(img_path, component)
    ev.click(compo)
