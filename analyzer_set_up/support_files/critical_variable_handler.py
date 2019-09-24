import tkinter as tk

class critical_variables():
    def __init__(self,File='default.txt'):
        self.variables = {}
        self.tk_variables = {}
        try:
            f = open(file,'r')
            defaults = f.read()
            f.close
            
            for line in defaults.splitlines():
                t=line.find(" = ")
                self.variables[line[:t]]=line[t+3:]
        except:
            pass
        

    def get_value(self,tag,default=''):
        if tag in self.variables:
            return self.variables[tag]
        else:
            self.variables[tag] = default
            return default
        
    def set_tk_input(self,tag,value=' '):
        self.tk_variables[tag] = tk.StringVar()
        if tag in self.variables:
            value=self.variables[tag]
        self.tk_variables[tag].set(value)

    def get_tk_input(self,tag,default=''):
        return self.tk_variable[tag].get()

    def allkeys(self):
        return list(self.variables.keys())

    def save_critical_values(self,file = 'default.txt'):
        with open(file,'w') as f:                
            for variable in self.tk_variables:
                
                line = '{0} = {1}\n'.format(variable,self.tk_variables[variable].get())
                f.write(line)

