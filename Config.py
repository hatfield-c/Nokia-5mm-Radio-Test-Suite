from modules.DumpInput import DumpInput
from modules.OBUE_Test import OBUE_Test
from modules.ACLR_Test import ACLR_Test
from modules.EVM_5GNR_Test import EVM_5GNR_Test
from modules.M_OBUE_Standard import M_OBUE_Standard
from modules.M_OBUE_Standard_Demo import M_OBUE_Standard_Demo

_CONFIG_ = {
    # App Configuration
    "app_title": "Test Suite Manager",
    "version": "0.96",

    # CSV Configuration
    "csv_dir": "CSV Data/",
    "result_dir": "CSV Data/Results/",
    "csv_path_key": "csv_path",
    "csv_child_data_key": "child_data",
    "csv_newline": "",

    # UI Color Definitions
    "color_primary": "#dbdbdb",
    "color_secondary": "#d4d4d4",
    "blue_primary": "#f7feff",

    # Media Paths
    "favicon_path": "media/icon.ico",
    "logo_path": "media/logo.gif",
    "icon_path": "media/icon_huge.gif",
    "flare_path": "media/flare.gif",
    "activate_path": "media/activate.gif",

    # Runtime Configuration
    "app_root": None,
    "working_dir": None,
    "current_suite_file": None,

    # Test Module Registration
    "modules": {
        "DumpInput": DumpInput,
        "OBUE": OBUE_Test,
        "EVM": EVM_5GNR_Test,
        "M_OBUE": M_OBUE_Standard,
        "M_OBUE_DEMO": M_OBUE_Standard_Demo,
        "ACLR": ACLR_Test
    }

}
