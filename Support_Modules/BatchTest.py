# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

import sys
sys.path.insert(0, '')

import tkinter as tk
from tkinter import filedialog
import openpyxl as pyxl
import csv

from Support_Modules import TestConfig as tcfg
from Support_Modules import ResultPane as rsp
from OBUE import OBUE_Test as obue
from EIRP import EIRP_Test as eirp
from NR_5G import EVM_5GNR_Test as evm

class BatchTester():


    version = 0.1
    output_file = ".//Results//autogen.csv"

    def __init__(self):

        root = tk.Tk()
        root.title("BatchRun %s"% self.version)

        root.filename = filedialog.askopenfilename(initialdir = "./TestCases")
        test_file = root.filename
        self.output_file_name = root.filename.strip()


        test_list = self.read_csv_lines(test_file)

        #read the testbench for all of the tests and send those down.
        self.test_conf = tcfg.TestConfig()
        self.testbench = self.test_conf.testbench_configuration

        #resutls are a tuple of (test_params, test_results)
        result_list = []
        #Test cases.
        for test_params in test_list:
            if test_params['TEST'] == "OBUE":
                obue_test_obj = obue.OBUE_Test(test_params, self.testbench,
                                                to_log = False)
                vals = obue_test_obj.run_test()
                result_list.append((test_params, vals))

            elif test_params['TEST'] == "EIRP":
                eirp_test_obj = eirp.EIRP_Test(test_params, self.testbench,
                                                to_log = False)
                vals = eirp_test_obj.run_test()
                result_list.append((test_params, vals))

            elif test_params['TEST'] == "EVM":
                evm_test_obj = evm.EVM_Test(test_params, self.testbench,
                                                to_log = False)
                vals = evm_test_obj.run_test()
                result_list.append((test_params, vals))

        #process result list by outputting to result pane?
        for test_res in result_list:
            test_result_pane = rsp.ResultPane(root, test_res)
            test_result_pane.pack()

        #ask for the save file
        root.filename = filedialog.asksaveasfile(initialdir = "./Results")
        self.output_file_name = root.filename

        #write to that save file
        self.write_testbench_boilerplate()
        self.add_test_results(result_list)

        root.mainloop()


    def read_csv_lines(self, test_file):

        #list to contain raw strings.
        fileline_list = []
        #read the file
        with open(test_file, "r") as f:
            raw_lines = f.readlines()

        #split all line along delimeter
        row_list = [] #place in row_list, 2d list created
        for line in raw_lines:
            row_list.append((line.strip()).split(","))

        #2d list representing the csv file.
        test_list = []
        for i in range(0, len(row_list) ):
            line_tag = ((row_list[i][0].strip()).upper())

            #if we find our sha bang #!
            if (line_tag == 'TEST'):
                attribute_row = row_list[i]
                i += 1 #increment
                data_row = row_list[i]

                #add testcase dictionary
                test_list.append(
                    self.merge_rows_to_dic(attribute_row, data_row))

        #returns test_list, a list of dics each dic corresponding to a
        #and essential parameters.
        print("END")
        return test_list


    #helper class
    def merge_rows_to_dic(self, attribute_row, data_row):

            test_case_dic = {}
            for index in range(0, len(attribute_row) ):
                test_case_dic[attribute_row[index]] = data_row[index]
            return test_case_dic


    #init log file
    def write_testbench_boilerplate(self):

        #log the self.testbench stuff
        with open (self.output_file, "w") as f:
            if self.testbench:
                #log self.testbench configuration before peak results.
                for attribute in self.testbench:
                    f.write(str(attribute))
                    f.write(",")
                    f.write(str(self.testbench[attribute]))
                    f.write('\n')
                f.write(',\n,\n') #spacing lines for .csv config.

    #append to log file
    def add_test_results(self, result_list):

        with open(self.output_file, "a") as f:
            for case in result_list:
                f.write(str(case[0]) + "," )
                f.write("\n")
            for case in result_list:
                f.write(str(case[1]) + "," )
                f.write("\n")


if __name__ == '__main__':

    #read a csv into a dictionary.
    #find a format for reading csv into columns.
    BatchTester()
