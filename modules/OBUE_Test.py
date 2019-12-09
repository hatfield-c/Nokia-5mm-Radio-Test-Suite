# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

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

#OBUE_T is the instance specific version of the test object
#containing all the necessary calculations and class fields to represent
#a OBUE test specification.

#will be displayed in the specification panels along with an
#instance run button, any alterations to the OBUE test will
#necessitate going through the initial OBUE_Window configuration and
#recalculating the parameters for the test.

class OBUE_Test():

    #10^9 hz from ghz
    RF_Start = 37.0
    RF_Stop = 40.0

    #TODO:
    #add some kind of try catch validation to stub out an unconnected test.
    #ERROR: plug things in or something like that.

    #paremeters includes center_freq_ghz,
    def __init__(self, parameters, testbench = None, to_log = True,
                    iq_swap = False):

        flatParameters = parameters
        flatTestbench = testbench
        parameters = Helper.DataController.GetDictionary(flatParameters)
        testbench = Helper.DataController.GetDictionary(flatTestbench)

        #each frequency has 4 spans. Will be stored as a dictionary of tuples.
        #enter Center Frequency from the beginning.
        self.fc = float(parameters['Center Frequency(GHz)'])
        self.ch_bw_mhz = int(parameters["Channel Bandwidth(MHz)"])
        self.rbw = int(parameters["Resolution Bandwidth(Hz)"])
        self.sweep_time = float(parameters["Sweep Time(s)"])
        self.testbench = testbench
        self.to_log = to_log
        self.iq_swap = iq_swap

        #where testbench is the secondary given parameter dictionary
        if self.testbench:
            self.RF_Start = float(self.testbench['RF Start'])
            self.RF_Stop = float(self.testbench['RF Stop'])

        #channel start and stop around fc calculated from offset to bandwidth
        self.ch_start = self.fc -((self.ch_bw_mhz/1000)/2)
        self.ch_stop = self.ch_start +(self.ch_bw_mhz/1000)

        #span of the bw
        self.span = int((self.ch_stop - self.ch_start)*(10**9))

        #calculate spans. This is modularized but is always part of the init
        #as span_list is a class variable.
        self.span_list = self.calc_spans()
        self.pf_limit = self.calculate_pf_limit()


    def run_test(self):
        peak_list = []

        index = 0
        for span in self.span_list:
            #test all spans with the same res.
            peak = obue_scpi.obue_script(("Span " + str(index)),
                                            self.sweep_time, self.rbw,
                                            span[0], span[1],
                                            self.testbench,
                                            iq_swap = self.iq_swap)
            #Calculate Additional Peak Info?
            #print(peak)
            peak_list.append(peak)
            index += 1


        #Compare TRP to P/F limit
        #span has an odd 0 1 function to loop. TODO: find more readable way to
        #do this .
        if(float(peak_list[0]['TRP']) > self.pf_limit[0]):
            peak_list[0]['P/F'] = "Fail"
        else:
            peak_list[0]['P/F'] = "Pass"

        if(float(peak_list[1]['TRP']) > self.pf_limit[1]):
            peak_list[1]['P/F'] = "Fail"
        else:
            peak_list[1]['P/F'] = "Pass"

        if(float(peak_list[2]['TRP']) > self.pf_limit[1]):
            peak_list[2]['P/F'] = "Fail"
        else:
            peak_list[2]['P/F'] = "Pass"

        if(float(peak_list[3]['TRP']) > self.pf_limit[0]):
            peak_list[3]['P/F'] = "Fail"
        else:
            peak_list[3]['P/F'] = "Pass"

        #PEAK LIST is a list of dictionaries containing test results
        return peak_list


    #NOTE: k constants are now indexed at 0, 0, 1 ,3 instead of the
    #k1, k2, k3 used in the SC OBUE Results Calculation .xlsx
    def calculate_pf_limit(self):

        #given
        array_qty = (256, 64)
        K_Constants = ((-5.0, 33.0, -12.0),(-13.0, 41.0, -20.0))
        element_gain = (5.0, 5.0)
        eirp_rated = (57.0, 51.0)

        pf_limit = [0, 0]

        #run indexed calculations for both array configurations.
        for i in range(0, 1):
            array_gain = (10*math.log(array_qty[i]))
            total_gain = array_gain + element_gain[i]
            #this is kind of a hack idk if its the way to go about calculating
            #this value.
            trp_rated = eirp_rated[i] - (i * 6)

            #min(k0, MAX(TRP_rated - k1, k2))
            k1_adjusted = trp_rated - K_Constants[i][1]

            if (k1_adjusted > K_Constants[i][2]):
                pf_limit[i] = k1_adjusted
            else:
                pf_limit[i] = K_Constants[i][2]

            if (K_Constants[i][0] < pf_limit[i]):
                pf_limit[i] = K_Constants[i][0]


        pf_limit = [-5.1, -13.1]
        return pf_limit


    def calc_spans(self):
        #spans go in order of increasing frequency but unlike the
        #SC OBUE Results Calculation Tests spreadsheet

        #       S T A R T  I N D E X I N G  A T  0      #

        #so thats different but its better this way.
        #todo: do some kind of guard to account for the inaccuracy generated
        #from shifting between float and integer.

        span = []

        #span0
        start0 = self.RF_Start - 1.5
        stop0 = self.ch_start - (0.1 * (self.ch_bw_mhz/1000)) + (0.5/1000)
        span0 = (start0, stop0)
        span.append(span0)

        #span1
        start1 = stop0
        stop1 = self.ch_start-(0.5/1000)
        span1 = (start1, stop1)
        span.append(span1)

        #span2
        start2 = self.ch_stop+(0.5/1000)
        stop2 = self.ch_stop+(0.1*(self.ch_bw_mhz/1000)) + (0.5/1000)
        span2 = (start2, stop2)
        span.append(span2)

        #span3 be updated later refer to test setup for >40GHz
        start3 = stop2
        stop3 = 40
        span3 = (start3, stop3)
        span.append(span3)

        return span
        #return list of spans. Each span is a tuple consisiting of
        #the start and then the stop fq in float GHz


    def print_test_config(self):
        #prints class variables used in the testing.
        print("Frequency Center: %s"%(self.fc))
        print("Channel Bandwidth: %s"%(self.ch_bw_mhz))
        print("Sweep time: %s"%(self.sweep_time))
        print("Channel Start: %s"%(self.ch_start))
        print("Channel Stop: %s"%(self.ch_stop))


    def return_configuration(self):
        #returns all class variables in a
        #neatly packaged and formatted dictioanry
        configuration = {}
        configuration["Frequency Center"] = self.fc
        configuration["Channel Bandwidth"] = self.ch_bw_mhz
        configuration["Sweep Time"] = self.sweep_time
        configuration["Channel Start"] = (str(round(float(self.ch_start), 5)) )
        configuration["Channel Stop"] = (str(round(float(self.ch_stop), 5)) )
        configuration["P/F Limit"] = self.pf_limit

        index = 0
        for span in self.span_list:
            span_name = "Span " + str(index)
            configuration[span_name] = ((str(round(float(span[0]), 5)) ),
                                        (str(round(float(span[1]), 5)) ) )
            index += 1
        return configuration #dictionary of attributes

#------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        testcase = OBUE_Test(37.40034, 100, 1000000, 0.2)
        testcase.run_test()
    	#TODO: Transfer Units to correct magnitude
        print("OBUE test should be configured main runs it with default testcase")

    except visa.VisaIOError:
        print("ERROR: Visa IO Error")
