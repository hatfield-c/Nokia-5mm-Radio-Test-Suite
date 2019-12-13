import modules.DumpInput
import modules.M_OBUE_Dump

import modules.OBUE_Test
import modules.M_OBUE_Test
import modules.EIRP_Test
import modules.EVM_5GNR_Test

_CONFIG_ = {
    # App Configuration
    "app_title": "Test Suite Manager",
    "version": "0.96",

    # CSV Read/Write Configuration
    "csv_path_key": "csv_path",
    "csv_child_data_key": "child_data",
    "csv_newline": "",

    # CSV Default Directories
    "csv_dir": "CSV Data/",
    "suite_dir": "CSV Data/Suites/",
    "collection_dir": "CSV Data/Collections/",
    "bench_dir": "CSV Data/Parameters/Benches/",
    "unit_dir": "CSV Data/Parameters/Units/",
    "sequence_dir": "CSV Data/Sequences/",
    "result_dir": "CSV Data/Results/",

    # Media Paths
    "favicon_path": "media/icon.ico",
    "logo_path": "media/logo.gif",
    "icon_path": "media/icon_huge.gif",
    "flare_path": "media/flare.gif",
    "activate_path": "media/activate.gif",

    # UI Color Definitions
    "color_primary": "#dbdbdb",
    "color_secondary": "#d4d4d4",
    "blue_primary": "#f7feff",

    # Runtime Configuration
    "app_root": None,
    "working_dir": None,
    "current_suite_file": None,

    # Test Module Registration
    "modules": {
        "DumpInput": modules.DumpInput.DumpInput,
        "M_OBUE_DUMP": modules.M_OBUE_Dump.M_OBUE_Dump,
        "OBUE": modules.OBUE_Test.OBUE_Test,
        "M_OBUE": modules.M_OBUE_Test.M_OBUE_Test,
        "EIRP": modules.EIRP_Test.EIRP_Test,
        "EVM": modules.EVM_5GNR_Test.EVM_5GNR_Test
    }

}
