#Anthony Tang
#Anthony.Tang@utdallas.edu
#       standard library imports
import sys
sys.path.insert(0, '')
import csv
import math
import datetime as dt

#       third party imports
import visa

#       local imports
from OBUE import OBUE_Script as obue_scpi
from Support_Modules import csv_logger as csvr


class M_OBUE_Test_A:

    RF_Start = 37.00 #37.00 GHz
    RF_Stop = 40.00 #40.00GHz

    f_offset_max_L = RF_Start - 1.5 #37GHz - 1.5 GHz
    f_offset_max_R = RF_Stop + 1.5 #40 GHz + 1.5 GHz


    def __init__(self, parameters, testbench = None, to_log = True,
                    iq_swap = False):

        #simplify the block of contiguous multicarrier to
        #a contiguous block tuple. (lower_bound, upper_bound)
        carrier_list = parameters['carrier_dic']

        lowest_carrier_span = calc_carrier_span(carrier_list[0])
        highest_carrier_span = calc_carrier_span(carrier_list[-1])

        carrier_block = (lowest_carrier_span[0], highest_carrier_span[1])
        self.BW_Contiguous = (carrier_block[1] - carrier_block[0]) * 1000

        self.sweep_time = parameters['Sweep Time(s)']
        self.rbw = parameters["Resolution Bandwidth(Hz)"]
        self.testbench = testbench
        self.iq_swap = iq_swap

        return

    #Where carrier is a dictionary containing
    #{fc_ghz, ch_bw_mhz}
    def calc_carrier_span(carrier):
        #channel start and stop around fc calculated from offset to bandwidth
        carrier['ch_bw_mhz']
        start = carrier['fc_ghz']- ((carrier['ch_bw_mhz']/1000)/2)
        stop = start + (carrier['ch_bw_mhz']/1000)
        return (start, stop)


    def calc_spans_a(self):
        #spans 0 through n left to right.
        bw_mid_offset = (0.1 *(self.BW_Contiguous) + 0.5)
        spans = []
        spans[0] = (self.f_offset_max_L,
                    self.carrier_block[0] - bw_mid_offset)

        spans[1] = (self.carrier_block[0] - bw_mid_offset,
                    self.carrier_block[0] - 0.5)

        spans[2] = (self.carrier_block[1] + 0.5,
                    self.carrier_block[1] + bw_mid_offset)

        spans[3] = (self.carrier_block[1] + bw_mid_offset,
                    self.f_offset_max_R)

        return spans

    def run_test(self):

        offset_spans = self.calc_spans_a()
        index = 0
        peak_list = []
        for span in offset_spans:
            peak = obue_scpi.obue_script(("Span " + str(index)),
                                            self.sweep_time, self.rbw,
                                            span[0], span[1],
                                            self.testbench,
                                            iq_swap = self.iq_swap)
            peak_list.append(peak)
            index += 1

        return peak_list

if __name__ == '__main__':

    test = OBUE_Test()
    test.run()
