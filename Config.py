from modules.DumpInput import DumpInput
from modules.OBUE_Test import OBUE_Test

_CONFIG_ = {
    # App Configuration
    "app_title": "Test Suite Manager",
    "version": "0.56",
    "favicon_path": "media/icon.ico",
    "logo_path": "media/logo.gif",

    # CSV Configuration
    "csv_dir": "CSV Data/",
    "csv_path_key": "csv_path",
    "csv_child_data_key": "child_data",
    "csv_newline": "",

    # UI Configuration
    "color_primary": "#dbdbdb",
    "color_secondary": "#d4d4d4",

    # Test Module Registration 
    "modules": {
        "DumpInput": DumpInput,
        "OBUE": OBUE_Test
    },

    # Runtime Configuration
    "app_root": None,
    "current_file": None,
    "working_dir": None
}
