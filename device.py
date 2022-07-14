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
        self.tmp_path = os.path.join("tmp", self.serial)
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    def connect(self):
        """
        Connect the device.
        :return:
        """
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

    def dump_2nd(self):
        """
        Get the UI hierarchy dump content.
        :return: The path of the hierarchy xml file.
        """
        path = os.path.join(self.tmp_path, "hierarchy.xml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.d.dump_hierarchy())
        return path



if __name__ == '__main__':
    dd = Device("emulator-5554")
    dd.connect()
    # dd.screenshot("test")
    print(dd.dump_2nd())
