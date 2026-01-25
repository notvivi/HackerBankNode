# Author: ChatGPT
# Date finished: 2025-27-11
import os
import sys

def resource_path(relative_path):
    """ Returns the absolute path to a given file.
    :param relative_path: Relative path to a file.
    :return: Absolute path to give a file. """
    if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)