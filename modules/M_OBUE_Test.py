#Anthony Tang
#Anthony.Tang@utdallas.edu
#       standard library imports
import sys
import csv
import math
import datetime as dt

#       third party imports
import visa

#       local imports
import modules.SCPI_Scripts.OBUE_Script as obue_scpi
import core.DataController as Helper

class M_OBUE_Test:

    RF_Start = 37.00 #37.00 GHz
    RF_Stop = 40.00 #40.00GHz
    MAX_CARRIERS = 8

    f_offset_max_L = RF_Start - 1.5 #37GHz - 1.5 GHz
    f_offset_max_R = RF_Stop + 1.5 #40 GHz + 1.5 GHz

    def __init__(self, parameters, testbench = None,
                    to_log = True, iq_swap = False):
        self.FAIL = False
        self.failures = []

        flatParameters = parameters
        flatTestbench = testbench
        parameters = Helper.DataController.GetDictionary(flatParameters)
        testbench = Helper.DataController.GetDictionary(flatTestbench)

        carrier_list = self.extract_carrier_vals(parameters)

        if not carrier_list or carrier_list is None:
            self.FAIL = True
            failure = { 
                "title": "EMPTY CARRIER LIST", 
                "message": "A list of carriers was not properly provided to this test class. Please ensure that carrier parameter data is properly set and not empty." 
            }
            self.failures.append(failure)

            return

        #simplify the block of contiguous multicarrier to
        #a contiguous block tuple. (lower_bound, upper_bound)
        #sort the carrier list by the carrier's frequency Center
        carrier_list = sorted(carrier_list, key=lambda x:
                                float(x['Center Frequency(GHz)']))

        #print("carrier list 0", carrier_list[0])
        #print("carrier list -1", carrier_list[-1])
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
        if str(parameters['Category']) == "1":
            #category_a
            print("A")
            self.offset_spans = self.calc_spans_a()

        if (parameters['Category']) == "2":
            #category b
            print("B")
            self.offset_spans = self.calc_spans_b()

        #print("spans", self.offset_spans)

    def run_test(self):
        if self.FAIL:
            return self.failures

        index = 0
        peak_list = []
        for span in self.offset_spans:
            peak = obue_scpi.obue_script(
                ("Span " + str(index)),
                float(self.sweep_time), 
                float(self.rbw_MHz),
                span[0], span[1],
                self.testbench,
                iq_swap = self.iq_swap
            )
            peak_list.append(peak)
            print(peak)
            index += 1
        return peak_list


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
        bw_mid_offset = (0.1 * (self.BW_Contiguous+ 0.0000005))
        spans = []

        spans.append((self.f_offset_max_L,
                    self.carrier_block[0] - bw_mid_offset))

        spans.append(((self.carrier_block[0]-bw_mid_offset),
                    (self.carrier_block[0] -(0.5/(10**6)))))

        spans.append(((self.carrier_block[1] + (0.5/(10**6))),
                    self.carrier_block[1] + bw_mid_offset))

        spans.append((self.carrier_block[1] + bw_mid_offset,
                    self.f_offset_max_R))

        return spans

    #Fix calc spans B. Calculating invalid band sizes.
    def calc_spans_b(self):

        #calculate 3 spans to each side
        bw_mid_offset = (0.1 * (self.BW_Contiguous+ 0.0000005))
        spans = []
        spans.append((self.f_offset_max_L,
                        (self.carrier_block[0]-((2*self.BW_Contiguous-0.000005)))))

        spans.append(( self.carrier_block[0] - (2*(self.BW_Contiguous - 0.0000005)),
                        (self.carrier_block[0]-bw_mid_offset)
                    ))

        spans.append(( (self.carrier_block[0] - bw_mid_offset),
                        (self.carrier_block[0]-0.0000005)
                    ))

        #Carrier Frequency Block

        spans.append(( (self.carrier_block[1] +(0.0000005)),
                     (self.carrier_block[1] + bw_mid_offset)
                    ))

        spans.append(( (self.carrier_block[1] + bw_mid_offset),
                        self.carrier_block[1] + (2*(self.BW_Contiguous-0.0000005))
                    ))

        spans.append(( self.carrier_block[1] + (2*self.BW_Contiguous+0.000005),
                        self.f_offset_max_R
                    ))

        return spans


    def extract_carrier_vals(self, parameters):
        carrier_list = []

        #iterate through carriers
        for carrier_num in range(0, self.MAX_CARRIERS):
            c_key = ("Carrier%d"%carrier_num)
            fc_key = ("Center Frequency(GHz)%d"%carrier_num)
            bw_key = ("Channel Bandwidth(MHz)%d"%carrier_num)
            carrier = {}

            if fc_key in parameters:
                if parameters[fc_key] is not None and parameters[fc_key] != "":
                    carrier["Center Frequency(GHz)"] = parameters[fc_key]
                
                parameters.pop(fc_key)

                if bw_key in parameters:
                    if parameters[bw_key] is not None and parameters[bw_key] != "":
                        carrier["Channel Bandwidth(MHz)"] = parameters[bw_key]
                    
                    parameters.pop(bw_key)

            if c_key in parameters:
                parameters.pop(c_key)

            if carrier:
                carrier_list.append(carrier)

        return carrier_list



if __name__ == '__main__':
    parameters = {}
    parameters['Category'] = "1"
    parameters['Resolution Bandwidth(MHz)'] = 1000
    parameters['Sweep Time(s)'] = 0.1

    carrier_list = [{'Center Frequency(GHz)': '36.5', 'Channel Bandwidth(MHz)': '1000'},
                    {'Center Frequency(GHz)': '36.6', 'Channel Bandwidth(MHz)': '1000'},
                    {'Center Frequency(GHz)': '36.7', 'Channel Bandwidth(MHz)': '1000'},
                    {'Center Frequency(GHz)': '36.8', 'Channel Bandwidth(MHz)': '1000'}]

    test = M_OBUE_Test_Contig(parameters, carrier_list)
