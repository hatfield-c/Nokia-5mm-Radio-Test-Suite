from modules.TestClass import TestClass
from modules.OBUE_Test import OBUE_Test

_CONFIG_ = {
    "app_title": "Nokia Test Suite Manager",
    "version": "0.56",
    "favicon": "media/icon.ico",
    "csv_dir": "CSV Data/",
    "csv_path_key": "csv_path",
    "csv_child_data_key": "child_data",
    "csv_newline": "",

    "app_root": None,
    "current_file": None,
    "working_dir": None,

    "color_primary": "#dbdbdb",
    "color_secondary": "#d4d4d4",

    "overseers": {
        "testing": TestClass,
        "OBUE": OBUE_Test
    }
}
