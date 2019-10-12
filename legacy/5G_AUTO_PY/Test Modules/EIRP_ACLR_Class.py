import STATION_globals as STATION

class EIRP_ACLR():

    #does the eirp aclr test. I guess.
    #attributes required for the eirp - aclr test.

    config_dict = {}

    #default values

    def __init__( self,
                    tx_channel_count = 1,
                    adj_channel_count = 2,
                    tx_bw = 95,
                    adj bw = 95,
                    center_freq = 39.0,
                    expected_rf_lvl = 0,
                    ref_lvl_offset = 65,
                    gate_delay = '262u',
                    gate_length = '97u' ):

        self.config_dict['tx_channel_count'] = tx_channel_count
        self.config_dict['adj_channel_count'] = adj_channel_count
        self.config_dict['tx_bw'] = tx_bw
        self.config_dict['adj_bw'] = adj_bw
        self.config_dict['center_freq'] = center_freq
        self.config_dict['expected_rf_lvl'] = expected_rf_lvl
        self.config_dict['ref_lvl_offset'] = ref_lvl_offset
        self.config_dict['gate_delay'] = gate_delay
        self.config_dict['gate_length'] = gate_length


    def set_analyzer_values():

        #i dont know if the order of this is a critical part
        #but at some point if it doesn't matter we should reorder
        #this so that all user input is grouped together.
        STATION.DEVICES['ANALYZER'].ACP('ACP')
        STATION.DEVICES['ANALYZER'].ACP_num_channels(
                                    self.config_dict['adj_channel_count'])
        STATION.DEVICES['ANALYZER'].power_channel_bandwidth(
                                    1, self.config_dict['TX BW'] )
        STATION.DEVICES['ANALYZER'].adjacent_channel_bandwidth(
                                    1, self.config_dict['ADJ BW'])
        STATION.DEVICES['ANALYZER'].power_channel_spacing(1,'99.84M')
        STATION.DEVICES['ANALYZER'].adjacent_channel_spacing(1, '100M')
        STATION.DEVICES['ANALYZER'].frequency(self.config_dict['center_freq'])
        STATION.DEVICES['ANALYZER'].span('1G')
        STATION.DEVICES['ANALYZER'].RBW('1M')
        STATION.DEVICES['ANALYZER'].VBW('AUTO')
        STATION.DEVICES['ANALYZER'].channel_power_mode(mode='ABS')
        STATION.DEVICES['ANALYZER'].channel_write_mode(write='WRIT')
        STATION.DEVICES['ANALYZER'].sweep_time_auto()
        STATION.DEVICES['ANALYZER'].sweep_mode(onoff='OFF')
        STATION.DEVICES['ANALYZER'].gated_trigger(source='EXT',
                                                  delay=self.config_dict['gate_delay'],
                                                  mode='LEV',
                                                  polatity='POS',
                                                  length=self.config_dict['gate_length']])
        STATION.DEVICES['ANALYZER'].trace_detector(trace=1,detector='RMS')
