import os, sys
import psse34
import psspy    
import redirect

def equivalent():
    global pp        
    redirect.psse2py()   
    psspy.psseinit(buses=1000)    
    psspy.case(r'D:\Google Drive\2_Benchmarking\Allen\models\PASF_SMIB_.sav')

    psspy.fdns(0)        
    psspy.flat_2([1,0,0,0,0,0,0,0],[0.0,0.0])

    psspy.cong(2)
    psspy.conl(0,1,1,[0,0],[ 100.0,0.0,0.0, 100.0])
    psspy.conl(0,1,2,[0,0],[ 100.0,0.0,0.0, 100.0])
    psspy.conl(0,1,3,[0,0],[ 100.0,0.0,0.0, 100.0])

    psspy.bsys(1,0,[0.0,0.0],0,[],2,[1011, 100],0,[],0,[])
    #psspy.bsys(1,0,[ 13.8, 500.],1,[1],0,[],0,[],0,[])        
    psspy.sceq(1,0,0, 10.0,"",r'D:\Google Drive\2_Benchmarking\Allen\models\PASF_SMIB_.r')

if __name__ == '__main__': 
    global pp      
    pp = r'D:\Google Drive\2_Benchmarking\Allen\models\\'
    equivalent()