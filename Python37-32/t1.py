
#global MEMORY
MEMORY=0

def command1():
    global MEMORY
    MEMORY = MEMORY+2
    _command2()
    print (MEMORY)
    
def _command2():
    global MEMORY

    MEMORY += 3
