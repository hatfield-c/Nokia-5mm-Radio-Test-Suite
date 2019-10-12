
import tkinter as tk
import time

class printWindow():
    def __init__(self,root,title,height=15,width=60,position='none',save_directory='none'):

        self.save=save_directory
        
        self.text_display_window = tk.Toplevel(root)
        ws = self.text_display_window.winfo_screenwidth()
        hs = self.text_display_window.winfo_screenheight()
        x = width*11
        y = height*20
        if position == 'upperright':
            self.text_display_window.geometry('%dx%d+%d+%d'%(x,y,ws-(x+15),0+10))
        self.text_display_window.title (title)
        self.myPrint = tk.Text(self.text_display_window,height=height,width=width)
        if save_directory != 'none':
            printbutton = tk.Button(self.text_display_window,text='print',command=self.savewindow)
            printbutton.grid(row=0,column=0,sticky='n')
        self.s = tk.Scrollbar(self.text_display_window)
        self.myPrint.grid(row=0,column=0)
        self.s.grid(row=0,column=1,sticky='nsw')

        self.s.config(command=self.myPrint.yview)
        self.myPrint.config(yscrollcommand=self.s.set)
        self.direction = 2

        self.myPrint.insert(tk.END,'summary\n\n')
        
        
        
    def Print(self,*text):
        for t in text:
           
            self.myPrint.insert(tk.END,str(t)+'\n')
            self.myPrint.see(tk.END)
            self.text_display_window.update()

                             

    def close(self):
        self.text_display_window.destroy()

    def savewindow(self):
        openedfile = open(self.save,'w')
        x=openedfile.write(self.myPrint.get("1.0",tk.END))
        openedfile.close()
                

        

if __name__ == '__main__': 
    
    p = printWindow("test1",
                    width=40,
                    height=5,
                    position='upperright')
    
    p.Print("1234567890123456789012345678901234567890")
    p.Print("one","two")

    
    time.sleep(3)
    p.close()
