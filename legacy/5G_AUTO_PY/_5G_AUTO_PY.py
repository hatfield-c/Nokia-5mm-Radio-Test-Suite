#python 3.7.3

#   Anthony Tang
#   Anthony.Tang@nokia.com

#   Manager: Joe Walker

#--------------------------------------------------------------------------
#                                  MAIN FUNCTION
#this python file contains the primary gui interface that the entire
#software suite should be accessible from. Central view exists here.
#--------------------------------------------------------------------------


import sys
import tkinter as tk

version = "6.05"

def do_math(X, Y):
    return (X + Y)

def run_obue_test(root):
    pass

def run_eirp_aclr_test(root):
    pass

def run_bem_test(root):
    pass

def run_eess_test(root):
    pass



#--------------------------------------------------------------------------
#                                  MAIN FUNCTION
#--------------------------------------------------------------------------
if __name__ == '__main__':

    #this should contain a dictionary of the test options. Develop tests
    #options individually using same module suite to easily allow the
    #addition of new tests.

    root = tk.Tk() #establish window.

    root.title('software version: %s'% version)
    main_frame = tk.Frame(root)
    main_frame.grid(row=0,column=0)

    #add butons
    obue_test_btn = tk.Button(main_frame, text = "OBUE",
                                command = lambda: run_obue_test(root))
    obue_test_btn.grid(row = 1, column = 0, sticky = tk.W)

    eirp_aclr_test_btn = tk.Button(main_frame, text = "EIRP-ACLR",
                                    command = lambda: run_eirp_aclr_test(root))
    eirp_aclr_test_btn.grid(row = 2, column = 0, sticky = tk.W)

    bem_test_btn = tk.Button(main_frame, text = "Block Edge Mass",
                            command = lambda: run_bem_test(root) )
    bem_test_btn.grid(row = 3, column = 0, sticky = tk.W)

    eess_test_btn = tk.Button(main_frame, text = "EESS",
                            command = lambda: run_eess_test(root) )

    eess_test_btn.grid(row = 4, column = 0, sticky = tk.W)

    #lets the GUI happen.
    root.mainloop()
