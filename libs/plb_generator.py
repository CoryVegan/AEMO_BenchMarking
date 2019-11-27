import os,sys
import psse34
import dyntools
import matplotlib.pyplot as plt
import pandas as pd
import glob

def  writePLBFile(FRT,DisDur_Time):   		
    try:
        import os
        plbFile = open('models\\zingen1.plb','w')
        plbFile.write('0,1,50\n')
        plbFile.write('10.999,1,50\n')
        plbFile.write('11,'+str(FRT)+',50\n')
        plbFile.write(str(11+DisDur_Time)+','+ str(FRT)+',50\n')
        plbFile.write(str(11+DisDur_Time+0.001)+',1,50\n')
        plbFile.write('22.0,1,50\n')
        plbFile.write('30.02,1,50\n')
        plbFile.close()		
    except:
        logerror()	
        
if __name__ == '__main__':
    FRT =         [1.3,  1.25, 1.225, 1.2, 1.118, 1.1, 0.9, 0.8, 0.7, 0.3]#Voltage disturbance at connection point
    DisDur_Time   = [0.06,  0.1,   0.2, 0.4,   0.9,  10,  10,   1,   2, 0.5]#Disturbance duration 
    DisStart_Time = 11
    RUN_Time = 25
    for i in range(len(FRT)):
        outputname='5.2.5.4'+'_['+str(FRT[i])+']_['+ str(DisDur_Time[i]) +']_'+'.out'
        writePLBFile(FRT[i],DisDur_Time[i]) 
        outputname = RunDynamics(FRT[i],DisDur_Time[i],RUN_Time)
        dynamic_plot_custom("outputs\\" + outputname)