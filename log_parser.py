import math
import os
import re
from utils import Utils


class LogParser:
    def __init__(self, tag):
        self.tag = tag
        self.matcher_timestamp = r"^(\d{1,4}-(?:1[0-2]|0?[1-9])-(?:0?[1-9]|[1-2]\d|30|31)) ((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d.\d{3})"

    def get_motion_event(self, log):
        """
        Get the timestamp and position of the motion event.
        :param log: A line from logcat.
        :return: A dictionary contains info about the motion event.
        """
        callback = "dispatchTouchEvent"
        key = "MotionEvent"
        position = tuple()
        if callback in log and key in log:
            obj = r"{ (.*) }"
            res = re.search(obj, log).group(1)
            pos_x = self.get_attribute(res, "x[0]")
            pos_y = self.get_attribute(res, "y[0]")
            position = (float(pos_x), float(pos_y))
        timestamp = re.search(self.matcher_timestamp, log).group()
        return {"timestamp": timestamp, "position": position}

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

    def view_calculate(self, log, hierarchy):
        """
        Calculate the interacted view in the hierarchy, with its bounds contain the position of the interaction.
        :param log: The line of logcat contains the position of the interaction.
        :param hierarchy: The xml hierarchy.
        :return: The calculated interacted view.
        """
        motion_event = self.get_motion_event(log)
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
        return view_cal

    @staticmethod
    def position_distance(position, x_min, y_min, x_max, y_max):
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        distance = math.sqrt((x_center - position[0]) ** 2 + (y_center - position[1]) ** 2)
        return distance


if __name__ == '__main__':
    logcat = "2022-07-11 20:57:06.552 11160-11160/com.example.appdemo I/MyWindowCallback: dispatchTouchEvent MotionEvent { action=ACTION_UP, actionButton=0, id[0]=0, x[0]=72.0, y[0]=583.0, toolType[0]=TOOL_TYPE_FINGER, buttonState=0, classification=NONE, metaState=0, flags=0x0, edgeFlags=0x0, pointerCount=1, historySize=0, eventTime=31962255, downTime=31962145, deviceId=0, source=0x1002, displayId=0 }"
    parser = LogParser("MyWindowCallback")
    hierarchy_path = os.path.join("tmp", "emulator-5554", "hierarchy.xml")
    parser.view_calculate(logcat, hierarchy_path)
