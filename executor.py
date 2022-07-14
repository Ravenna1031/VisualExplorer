import random

from device import Device
from airtest.core.api import *
from utils import Utils
from image import Image


class Executor:
    class Visual:

        def __init__(self, device):
            """
            To executor visual(3rd gen) test cases.
            :param device: The device to execute.
            """
            self.device = device

        def connect(self):
            init_device("Android")
            connect_device(f"android:///{self.device.serial}")

        @staticmethod
        def start_app(app):
            start_app(app)

        @staticmethod
        def click(target):
            """
            Use the image of a component to click.
            :param target: The path of a cropped image.
            :return: None
            """
            touch(Template(target, target_pos=5))

        @staticmethod
        def random_select_component(output):
            """
            Randomly select one component from all components.
            :param output: The path of visual detection result file.
            :return: One randomly chosen component.
            """
            components = Utils.get_all_visual_components(output)
            return random.choice(components)

    class Layout:
        pass
