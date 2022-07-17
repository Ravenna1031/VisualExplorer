import math
import subprocess

from loguru import logger
import re
from utils import Utils
from device import Device


class LogParser:
    def __init__(self, device):
        self.device = device
        self.matcher_timestamp = r"^((?:1[0-2]|0?[1-9])-(?:0?[1-9]|[1-2]\d|30|31)) ((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d.\d{3})"
        self.hierarchy = None

    def set_hierarchy(self, hierarchy):
        self.hierarchy = hierarchy

    def get_motion_event(self, line):
        """
        Get the timestamp and position of the motion event.
        :param line: A line from logcat.
        :return: A dictionary contains info about the motion event.
        """
        obj = r"{ (.*) }"
        res = re.search(obj, line).group(1)
        pos_x = self.get_attribute(res, "x[0]")
        pos_y = self.get_attribute(res, "y[0]")
        position = (float(pos_x), float(pos_y))
        timestamp = re.search(self.matcher_timestamp, line).group()
        result = {
            "timestamp": timestamp,
            "position": position
        }
        logger.info(f"Motion Event: {result}")
        self.view_calculate(result, self.hierarchy)
        return result

    @staticmethod
    def get_attribute(text, key):
        """
        Get attribute from a MotionEvent object.
        :param text: The text of the object.
        :param key: The name of the attribute.
        :return: The value of the attribute.
        """
        assert key in text, "Key not found."
        for i in text.split(" "):
            if "[" in key and "]" in key:
                tmp_key = key.replace("[", "\\[").replace("]", "\\]")
                matcher = f"{tmp_key}=" + r"(.*)"
            else:
                matcher = f"{key}=" + r"(.*)"
            if re.search(matcher, i):
                res = re.search(matcher, i).group(1)
                return res[:-1] if "," in res else res

    def view_calculate(self, motion_event, hierarchy):
        """
        Calculate the interacted view in the hierarchy, with its bounds contain the position of the interaction.
        :param motion_event: Motion event object with timestamp and position.
        :param hierarchy: The xml hierarchy.
        :return: The calculated interacted view.
        """
        # motion_event = self.get_motion_event(log)
        position = motion_event["position"]
        views = Utils.get_all_views(hierarchy)
        min_val = math.inf
        view_cal = None
        for view in views:
            x_min, y_min, x_max, y_max = view.get_x_y()
            if x_min < position[0] < x_max and y_min < position[1] < y_max:
                if self.position_distance(position, x_min, y_min, x_max, y_max) < min_val:
                    view_cal = view
                    min_val = self.position_distance(position, x_min, y_min, x_max, y_max)
        logger.info(
            f"Calculated View: index={view_cal.index}, text={view_cal.text}, "
            f"resource-id={view_cal.resource_id}, class={view_cal.class_name}")
        view_info = view_cal.get_all_attributes()
        Utils.record_sequence(view_info, self.device.sequence_path)
        return view_cal

    @staticmethod
    def position_distance(position, x_min, y_min, x_max, y_max):
        """
        The distance between two positions.
        :param position: A tuple contains x and y coordinate of a motion event.
        :param x_min: x_min value of a view.
        :param y_min: y_min value of a view.
        :param x_max: x_max value of a view.
        :param y_max: y_max value of a view.
        :return: The distance between.
        """
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        distance = math.sqrt((x_center - position[0]) ** 2 + (y_center - position[1]) ** 2)
        return distance

    def log_filter(self, tag, keywords):
        """
        Filter logs contain all the tag and keywords.
        :param tag: The tag of the log.
        :param keywords: Keywords to filter the log.
        :return:
        """
        self.log_clear()
        logger.info("Logcat Filter Start.")
        cmd = f"adb -s {self.device.serial} shell logcat"
        output = subprocess.Popen(args=cmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        with output:
            for line in output.stdout:
                line = line.decode("utf-8")
                if tag in line and self.check_keywords(line, keywords):
                    self.get_motion_event(line)

    @staticmethod
    def check_keywords(line, keywords):
        """
        Check if the line contains all the keywords.
        :param line: One line from the log.
        :param keywords: A list of keywords.
        :return: If the line contains the keywords.
        """
        if len(keywords) == 0:
            return True
        else:
            for keyword in keywords:
                if keyword not in line:
                    return False
            return True

    def log_clear(self):
        logger.info("Clear logcat.")
        cmd = ["adb", "-s", self.device.serial, "shell", "logcat", "-c"]
        subprocess.run(cmd)


if __name__ == '__main__':
    dd = Device("emulator-5554")
    dd.connect()
    parser = LogParser(dd)
    parser.log_filter(tag="MyWindowCallback", keywords=["dispatchTouchEvent", "MotionEvent", "action=ACTION_UP"])
