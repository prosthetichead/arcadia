import os
import sys

# --- PATH SETUP ---
if getattr(sys, 'frozen', False):
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.dirname(CURRENT_DIR)
    ROOT_DIR = os.path.dirname(SRC_DIR)

from shared.data_manager import DataManager

# Initialize DataManager (Singleton-ish)
data_manager = DataManager(ROOT_DIR)

def get_data_manager():
    return data_manager