import sys
import threading
import os
import time

from device import Device
from log_parser import LogParser
from executor import Executor
from image import Image


def execution(event_num):
    # step: take a screenshot of the device.
    # step: using GUI detection tool to get all the components on the screenshot.
    detection_result = os.path.join("example", "result.json")
    for i in range(event_num):
        # dump hierarchy before action event
        dumped_hierarchy = d.dump_2nd()
        parser.set_hierarchy(dumped_hierarchy)
        # randomly select a component from the detection result
        component = ev.random_select_component(detection_result)
        screenshot = Image(os.path.join("example", "05.png"))
        cropped_screenshot = os.path.join("example", "result.jpg")
        # using the info of selected component to crop the component from the screenshot.
        cropped_component = screenshot.crop_component(cropped_screenshot, component)
        # using the cropped component to interact with the component
        ev.click(cropped_component)
        time.sleep(5)


def main():
    tag = "MyWindowCallback"
    keywords = ["dispatchTouchEvent", "MotionEvent", "action=ACTION_UP"]
    # start a thread to filter logcat.
    thread_filter = threading.Thread(target=parser.log_filter, args=(tag, keywords,))
    thread_filter.start()
    execution(5)
    # # start a thread to execute actions
    # thread_execution = threading.Thread(target=execution, args=(5,))
    # thread_execution.start()


if __name__ == '__main__':
    d = Device("emulator-5554")
    d.connect()
    parser = LogParser(d)
    ev = Executor.Visual(d)
    ev.connect()
    main()
