import os

# --- PATH SETUP ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)

from shared.data_manager import DataManager

# --- CONFIG ---
ROOT_DIR = os.path.dirname(SRC_DIR)

# Initialize DataManager (Singleton-ish)
data_manager = DataManager(ROOT_DIR)

def get_data_manager():
    return data_manager