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
import OBUE_Script as obue_scpi
from Support_Modules import csv_logger as csvr


class M_OBUE_Test_Contig:

    RF_Start = 37.00 #37.00 GHz
    RF_Stop = 40.00 #40.00GHz

    f_offset_max_L = RF_Start - 1.5 #37GHz - 1.5 GHz
    f_offset_max_R = RF_Stop + 1.5 #40 GHz + 1.5 GHz


    def __init__(self, parameters, carrier_list, testbench = None,
                    to_log = True, iq_swap = False):
        print(parameters)
        #simplify the block of contiguous multicarrier to
        #a contiguous block tuple. (lower_bound, upper_bound)

        print(carrier_list)
        print("carrier list 0", carrier_list[0])
        print("carrier list -1", carrier_list[-1])
        lowest_carrier_span = self.calc_carrier_span(carrier_list[0])
        highest_carrier_span = self.calc_carrier_span(carrier_list[-1])

        self.carrier_block = (lowest_carrier_span[0], highest_carrier_span[1])
        print(self.carrier_block)

        self.BW_Contiguous = (self.carrier_block[-1] - self.carrier_block[0])

        self.sweep_time = parameters['Sweep Time(s)']
        self.rbw_MHz = parameters["Resolution Bandwidth(MHz)"]
        self.testbench = testbench
        self.iq_swap = iq_swap

        self.offset_spans = []
        print("Category", parameters['Category'])
        if parameters['Category'] == "1":
            #category_a
            print("A")
            self.offset_spans = self.calc_spans_a()

        if parameters['Category'] == "2":
            #category b
            print("B")
            self.offset_spans = self.calc_spans_b()

        print(self.offset_spans)

        self.run_test()

        return

    #Where carrier is a dictionary containing
    #{fc_ghz, ch_bw_mhz}
    def calc_carrier_span(self, carrier):
        carrier_fc = float(carrier['Center Frequency(GHz)'])
        channel_bw = float(carrier['Channel Bandwidth(MHz)'])
        #channel start and stop around fc calculated from offset to bandwidth
        start = carrier_fc - ((channel_bw/1000)/2)
        stop = start + (channel_bw/1000)
        return (start, stop)


    def calc_spans_a(self):
        #spans 0 through n left to right.
        bw_mid_offset = (0.1 *(self.BW_Contiguous) + 0.5)
        spans = []
        print(self.carrier_block)
        spans.append((self.f_offset_max_L,
                    self.carrier_block[0] - bw_mid_offset))

        spans.append((self.carrier_block[0] - bw_mid_offset,
                    self.carrier_block[0] - 0.5))

        spans.append((self.carrier_block[1] + 0.5,
                    self.carrier_block[1] + bw_mid_offset))

        spans.append((self.carrier_block[1] + bw_mid_offset,
                    self.f_offset_max_R))

        print("Calc spans A", spans)
        return spans

    def calc_spans_b(self):

        #calculate 3 spans to each side
        bw_mid_offset = (0.1 *(self.BW_Contiguous) + 0.5)
        spans = []
        spans.append((self.f_offset_max_L,
                    (self.carrier_block[0] - 2*self.BW_Contiguous+5)))

        spans.append((2*self.BW_Contiguous,
                    self.carrier_block[0]-bw_mid_offset))

        spans.append((self.carrier_block[0] - bw_mid_offset,
                    self.carrier_block[0]-0.5))

        #Carrier Frequency Block

        spans.append((self.carrier_block[1] + 0.5,
                    self.carrier_block[1] + bw_mid_offset))

        spans.append((self.carrier_block[1] + bw_mid_offset,
                    2*self.BW_Contiguous + 0.5))

        spans.append((2*self.BW_Contiguous + 5.0,
                    self.f_offset_max_R))

        print("Calc spans B", spans)
        return spans


    def run_test(self):

        index = 0
        peak_list = []
        for span in self.offset_spans:
            peak = obue_scpi.obue_script(("Span " + str(index)),
                                            self.sweep_time, self.rbw_MHz,
                                            span[0], span[1],
                                            self.testbench,
                                            iq_swap = self.iq_swap)
            peak_list.append(peak)
            index += 1

        return peak_list


if __name__ == '__main__':
    parameters = {}
    parameters['Category'] = "1"
    parameters['Resolution Bandwidth(MHz)'] = 1000
    parameters['Sweep Time(s)'] = 0.1

    carrier_list = [{'Center Frequency(GHz)': '26', 'Channel Bandwidth(MHz)': '1000'},
                    {'Center Frequency(GHz)': '27', 'Channel Bandwidth(MHz)': '1000'},
                    {'Center Frequency(GHz)': '28', 'Channel Bandwidth(MHz)': '1000'},
                    {'Center Frequency(GHz)': '29', 'Channel Bandwidth(MHz)': '1000'}]

    test = M_OBUE_Test_Contig(parameters, carrier_list)
