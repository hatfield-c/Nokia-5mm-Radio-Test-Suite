import tkinter as tk
import os,sys
from tkinter import messagebox
import time


def spreadsheet_file_2_array(Filename,delimiter='\t',Filter=''):
    
    try:
        openedfile = open(Filename,'r')
        filedata = openedfile.read()
        openedfile.close()
        array=[]
        array = map(lambda x:x.split(delimiter),filedata.splitlines())
        
        result=filter(lambda x:(x[0] == Filter)or(Filter==''),array)
    except:
        print ("error opening file {0} for read").format(Filename)
        result = []

    return result

    
def save_xydata(xydata,filename):
    
    try:
        openedfile = open(filename,'w')
        s = map (lambda x,y:str(x)+"\t"+str(y)+"\n",xydata[0],xydata[1])
        string =reduce (lambda filestring,x: filestring+x,s)
        openedfile.write(string)
        openedfile.close()
    except:
        print ("failed to write to file")

    return


class DirSearch():
    #dirwindow = tk.Tk()
    #currentdir=tk.StringVar()
    
    def __init__(self,D):

        #
        dirwindow = tk.Tk()
        root = tk.Frame(dirwindow)
        root.grid(row=0,column=0)

        #
        sb = tk.Scrollbar(root)
        sb.grid(row=3, column=1,sticky='nsw')
        #
        choices = tk.Listbox(root,width=40,height=25,yscrollcommand=sb.set)
        choices.grid(row=3,column=0)
        choices.bind("<Double-Button-1>",lambda event:self.select(self,choices,files))
        sb.config(command=choices.yview)
        choicelabel=tk.Label(root,text='directories')
        choicelabel.grid(row=2,column=0)
        #
        fb = tk.Scrollbar(root)
        fb.grid(row=3,column=4,sticky='nsw')
        #
        files = tk.Listbox(root,width=30,height=25,yscrollcommand=fb.set,fg='red')
        files.grid(row=3,column=2)
        fb.config(command=files.yview)
        fileslabel=tk.Label(root,text='files')
        fileslabel.grid(row=2,column=2)
        #
        doneButton=tk.Button(root,text="done",command = lambda : self.cleanup(dirwindow,files))
        doneButton.grid(row=1,column=0,sticky='ew')

        self.currentdir = tk.StringVar()
        self.selectedFile = 'DefaultFile.txt'
        
        current = tk.Label(root,textvariable=self.currentdir,width=30,height=1,)
        self.currentdir.set(D)
        current.grid(row=0,column=0)        
        choices.insert(tk.END,"..")

        for d in os.listdir(D):
            path = os.path.join(D,d)
            if os.path.isdir(path):
                choices.insert(tk.END,d)
            else:
                files.insert(tk.END,d)
        
        root.mainloop()


    def cleanup(self,dirwindow,filelistbox):
        if filelistbox.curselection() != ():self.selectedFile=filelistbox.get(filelistbox.curselection())
        dirwindow.destroy()
        dirwindow.quit()
        
    def get_info(self):
        return (self.currentdir.get(),self.selectedFile)
        
    def select(event,self,c,files):

        dirChoice = c.get(c.curselection())
        baseDir = self.currentdir.get()

        
        if dirChoice == '..':
           lastdir =  baseDir.rfind('\\',0,len(baseDir)-1)
           if lastdir > 1 : baseDir = baseDir[0:lastdir]+'\\'
           
           print (lastdir)
           D = baseDir
           self.currentdir.set(D)
        else:
            self.currentdir.set(baseDir+dirChoice+"\\")
            D = self.currentdir.get()
            
            
        c.delete(1,tk.END)
        files.delete(1,tk.END)
        try:
            for d in os.listdir(D):
                if os.path.isdir(os.path.join(D,d)):
                    c.insert(tk.END,d)
                else:
                    files.insert(tk.END,d)
                
        except WindowsError as g:
            message = "top secret....not for you"
            lastdir =  D.rfind('\\',0,len(baseDir)-1)
            if lastdir > 1 : baseDir = baseDir[0:lastdir]+'\\'

            tkMessageBox.showinfo(" ",message)
            D=baseDir
            self.currentdir.set(D)
            for d in os.listdir(D):
                if os.path.isdir(os.path.join(D,d)):c.insert(tk.END,d)
            
       
def save_xy_file(data,extension,path):
    
    datafile = open(path,'w')
    tdstring = reduce(lambda x,y:x+y,map(lambda x,y:str(x)+'\t'+str(y)+'\r\n',data[0],data[1]))
    
    datafile.write(tdstring)
    datafile.close()
    return path
    
def build_timedate():
    timedate=time.localtime()
     
    t=str(timedate[1])+'_'+\
    str(timedate[2])+'_'+\
    str(timedate[0])+'_'+\
    str(timedate[3])+'_'+\
    str(timedate[4])+'_'

    return t
    
if __name__ == ('__main__'):
    

    
    
    d='c:\\'
    
    #print DirSearch(d).currentdir.get()
    x= DirSearch(d)
    print (x.get_info())
    print (x.selectedFile)
    
   
    
    
