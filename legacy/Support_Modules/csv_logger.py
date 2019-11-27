# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

import datetime as dt

def log_to_csv(feedback_list, testbench = None, test_type = "Undefined"):

    if testbench:
        #pick a time and set it to the testbench attribute
        testbench['Test Date'] = str(dt.datetime.now().strftime(
                                                    '%H_%M_%S_%Y_%m_%d'
                                    ))

        #test should internally log results to csv,
        #return passed values should be used in GUI

        #generate name
        filename = test_type
        filename += "_"
        filename += str(testbench['Unit Name']) + "_"
        filename += str(testbench['Unit HW Version']) + "_"
        filename += str(testbench['TRX Module Version']) + "_"
        filename += str(testbench['Antenna Module Version']) + "_"
        filename += str(testbench['Carrier Configuration']) + "_"
        filename += str(testbench['Az. Beam Position']) + "_"
        filename += str(testbench['El. Beam Position']) + "_"
        filename += str(testbench['Test Date']) + "_"
        filename += ".csv" #still a csv
        filename = ".\\Results\\" + filename
        print(filename)

    else:
        filename = "default_test_log.csv"

    with open (filename, "w") as f:
        if testbench:
            #log testbench configuration before peak results.
            for attribute in testbench:
                f.write(str(attribute))
                f.write(",")
                f.write(str(testbench[attribute]))
                f.write('\n')
            f.write(',\n,\n') #spacing lines for .csv config.
        for key in feedback_list[0].keys():
            f.write(key + ",")
        f.write("\n")

        for peak in feedback_list:
            for field in peak:
                f.write(str(peak[field]) + "," )
            f.write("\n")
    return


if __name__ == '__main__':

    num = str(dt.datetime.now().strftime(
                                    '%H_%M_%Y_%m_%d'
                                ))
    print(num)
