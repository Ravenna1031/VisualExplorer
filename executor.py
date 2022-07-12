from device import Device
from airtest.core.api import *


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

    class Layout:
        pass


if __name__ == '__main__':
    dd = Device("emulator-5554")
    ev = Executor.Visual(dd)
    ev.connect()
    ev.start_app("com.example.appdemo")
    ev.click("01.png")
