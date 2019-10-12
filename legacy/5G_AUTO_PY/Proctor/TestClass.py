#   Anthony Tang
#   Anthony.Tang@nokia.com

#standard library imports
import os
import csv

#third party imports

#local imports

class TestClass():

    configurations = {}
    attributes = []

    def __init__(self, test_conf_file, directory_path, root):

        #on read. Read the first row of a csv. Each comma seperate value
        #corresponds to an attribute of the text class.
        with open( (directory_path + "/" + test_conf_file),
                    mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rowcount = 0;
            for row in csv_reader:
                self.configurations[row['Name']] = row
                if not self.attributes:
                    self.attributes = row.keys()

        #make a button field pair for each of the attributes in each config.


if __name__ == "__main__":
    #idk dont do anything this shouldn't happen
    #the test case class was intended as an aggregation class
    #dont do this.

    root = tk.Tk() #establish window.
    root.title('testclass')

    root.mainloop()
