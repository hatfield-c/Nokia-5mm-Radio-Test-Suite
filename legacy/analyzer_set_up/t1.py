# test of passing parameters using pointer

import t2

x=[1,2,3]

def call1(*alist):
    for a in alist:
        print ('inside call {0}'.format(a))
    
    

call1(1,[1,2,3],'test')
