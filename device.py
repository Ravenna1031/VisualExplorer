import uiautomator2 as u2
import os


class Device:
    def __init__(self, serial):
        self.serial = serial
        self.connection = False
        self.d = None
        self.screenshot_path = os.path.join("Output", "screenshot", self.serial)
        if not os.path.exists(self.screenshot_path):
            os.makedirs(self.screenshot_path)

    def connect(self):
        self.d = u2.connect(self.serial)
        self.connection = True

    def screenshot(self, name):
        """
        Take a screenshot and save to screenshot directory.
        :param name: Name of the saved image.
        :return:
        """
        assert self.connection, "Please connect device."
        image_path = os.path.join(self.screenshot_path, f"{name}.jpg")
        image = self.d.screenshot()
        image.save(image_path)


if __name__ == '__main__':
    dd = Device("emulator-5554")
    dd.connect()
    dd.screenshot("test")
