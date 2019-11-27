# File:"C:\Users\Z003SARM\Documents\working folder\Projects\Project Bulgana\2017_11_24 BGWF Conn Pkg - Gamesa 3.65MW\[1] RUG\PSSE V34 Model Files\Auto123.py", 
# generated on TUE, FEB 13 2018  15:02, PSS(R)E release 34.03.01
from libs.dynamic_plot import *
import time
import shutil
now = str(int(time.time()))

dirs = os.listdir(os.getcwd())

def logerror(error=None):
    import datetime
    import traceback
    """
    Allow user to log either a text error or
    open the last exception and log the traceback to a file.

    Essentially a quick work around.
    """
    errorfile = open('mainerror.log', 'a')
    now = datetime.datetime.now
    errorfile.write(now().strftime('%d-%b-%y %H:%M:%S') + '\n')

    if error is None:
        traceback.print_exc(file=errorfile)
    else:
        errorfile.write(str(error))

    errorfile.write('\n\n\n')
    errorfile.close()
        
def cleanUp(proj):
    import os
    homedir = os.path.abspath('.')
    for rootdir, dirs, files in os.walk(homedir):
        for file in files:
            base,ext = os.path.splitext(file)
            if ext == '.txt' or ext == '.log':
                try: 
                    os.remove(file)
                except:
                    logerror    

    # try:
    #     shutil.rmtree('outputs/{}'.format(proj))
    # except:
    #     pass
        
    # try:
    #     shutil.rmtree('plt/{}'.format(proj))
    # except:
    #     pass
    if os.path.isdir('outputs/{}'.format(proj)):
        shutil.rmtree('outputs/{}'.format(proj))
    if os.path.isdir('plt/{}'.format(proj)):
        shutil.rmtree('plt/{}'.format(proj))
        
    if not os.path.isdir('outputs/{}'.format(proj)):
        os.mkdir('outputs/{}'.format(proj))
    if not os.path.isdir('plt/{}'.format(proj)):
        os.mkdir('plt/{}'.format(proj))

def RunDynamics_PLB(FRT,DisDur_Time,RUN_Time, proj):
    try:
        import os,sys
        # PSSE_LOCATION = r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27"
        # sys.path.append(PSSE_LOCATION)
        # os.environ['PATH'] = os.environ['PATH'] + ';' +  r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN"
        import psse34
        import psspy
        import redirect
        parent_dir = os.getcwd()
        os.chdir('models/{}'.format(proj))
        if proj == 'PLSF':
            sav_file = 'PLSF_PE.sav'
            sav_cnv_file = 'PLSF_PE_cnv.sav'
            dyr_file = 'PLSF_PE_H1006D_Syncon_zingen.dyr'
            snp_file = 'PLSF_PE.snp'
            dll_file1 = 'PE_v34_2_H1006D.dll'
            dll_file2 = None#'SG3400HV_V28B10.dll'
            POC = 1150
            Inv = 1180
            Inv2 = 1181
            SIMB = 1130
            POC_Dummy = 1140
        elif proj == 'SGMODEL':
            sav_file = 'PLSF_PE_PLB.sav'
            sav_cnv_file = 'PASF_SMIB_cnv.sav'
            dyr_file = 'PASF_SMIB_zingen.dyr'
            snp_file = 'PASF_SMIB.snp'
            dll_file1 = 'SG3400HV_V28B10.dll'
            dll_file2 = 'INACES-V28.0.dll'
            POC = 1011
            Inv = 1
            Inv2 = -1#1181
            SIMB = 1000
            POC_Dummy = 1000
        else:
            raise("wrong proj name")

        redirect.reset()
        redirect.psse2py()
        _i=psspy.getdefaultint()
        _f=psspy.getdefaultreal()
        _s=psspy.getdefaultchar()
        psspy.psseinit()
        outputname=now +'_'+ '5.2.5.4'+'_['+str(FRT)+']_['+ str(DisDur_Time)+']'+  '.out'
        recdFN=now +'_'+ '5.2.5.4'+'_['+str(FRT)+']_['+ str(DisDur_Time)+']'+'.recd'
        #psspy.lines_per_page_one_device(1,60)
        psspy.progress_output(2,parent_dir + "\\outputs\\{}\\".format(proj) + recdFN,[0,0])
        # psspy.lines_per_page_one_device(1,60)
        psspy.prompt_output(2,parent_dir + "\\outputs\\{}\\".format(proj) + recdFN,[0,0])
        #psspy.lines_per_page_one_device(1,60)
        psspy.alert_output(2,parent_dir + "\\outputs\\{}\\".format(proj) + recdFN,[0,0])
        #psspy.addmodellibrary(r"""GMD0352_v34.dll""")
        #psspy.addmodellibrary(r"""GC0520T_v34.dll""")
        #psspy.case(r"""BGWF_Gamesa_SMIB_R6_FRT.sav""")
        psspy.addmodellibrary(dll_file1)
        if dll_file2 != None:
            psspy.addmodellibrary(dll_file2)
        # print(sav_file)
        # raise
        psspy.case(sav_file)
        psspy.solution_parameters_4([_i,99,_i,_i,_i],[_f,_f,_f,_f,_f, 1e-05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f, 1e-05,_f,_f])
        psspy.fnsl([0,0,0,0,0,0,99,0])
        psspy.cong(0)
        psspy.conl(0,1,1,[0,0],[ 100.0,0.0,0.0, 100.0])
        psspy.conl(0,1,2,[0,0],[ 100.0,0.0,0.0, 100.0])
        psspy.conl(0,1,3,[0,0],[ 100.0,0.0,0.0, 100.0])
        psspy.ordr(0)
        psspy.fact()
        psspy.tysl(0)
        psspy.save(sav_cnv_file)
        psspy.dyre_new([1,1,1,1],dyr_file,r"""CONEC.flx""",r"""CONET.flx""","")
        psspy.dynamics_solution_param_2([1000,_i,_i,_i,_i,_i,_i,_i],[0.1 ,1e-06, 0.001,0.02,_f,_f,_f,_f])


        v_ppc = r"""V_POC_PASF"""
        v_inv = r"""V_PASF"""
        Edf_smib = r'SMIB_EDF'
        UUT_smib = r'SMIB_UUT'
        P_smib = r'SMIB_PELEC'
        Q_smib = r'SMIB_QELEC'
        power_inv = [r"""P_PASF""", r"""Q_PASF"""]
        power_ppc = [r"""P_POC_PASF""",r"""Q_POC_PASF"""]
        v_plot = {'POC Power Profile': [power_ppc, 'MW/MVAR'], 
                    'Inverter Power Profile': [power_inv, 'MW/MVAR'], 
                    'V int':[v_inv, 'p.u.'], 
                    'V ppc':[[v_ppc, UUT_smib, Edf_smib], 'p.u.'], 
                    'V SMIB':[Edf_smib, UUT_smib, 'p.u.'], 
                    'Power SMIB':[P_smib, Q_smib, 'p.u.'], }
        psspy.voltage_channel([-1,-1,-1,POC],v_ppc)
        if Inv2 > 0:
            v_inv = r"""V_PASF_{}""".format(Inv)
            v_inv2 = r"""V_PASF_{}""".format(Inv2)
            power_inv = [r"""P_PASF_{}""".format(Inv), r"""Q_PASF_{}""".format(Inv)]
            power_inv2 = [r"""P_PASF_{}""".format(Inv2), r"""Q_PASF_{}""".format(Inv2)]
            v_plot = {'POC Power Profile': [power_ppc, 'MW/MVAR'], 
                        'Inverter Power Profile @{}'.format(Inv): [power_inv, 'MW/MVAR'], 
                        'Inverter Power Profile @{}'.format(Inv2): [power_inv2, 'MW/MVAR'], 
                        'V int @{}'.format(Inv):[v_inv, 'p.u.'], 
                        'V int @{}'.format(Inv2):[v_inv2, 'p.u.'], 
                        'V ppc':[[v_ppc, UUT_smib, Edf_smib], 'p.u.'],
                        'Efd SMIB':[Edf_smib, 'p.u.'], 
                        'Power SMIB':[P_smib, Q_smib, 'p.u.'], }
        print(v_plot)
        psspy.voltage_channel([-1,-1,-1,POC],v_ppc)
        psspy.machine_array_channel([-1,5,SIMB],r"""1""", Edf_smib) 
        psspy.machine_array_channel([-1,4,SIMB],r"""1""", UUT_smib) 
        psspy.machine_array_channel([-1,3,SIMB],r"""1""", Q_smib)
        psspy.machine_array_channel([-1,2,SIMB],r"""1""", P_smib)
        psspy.branch_p_and_q_channel([-1,-1,-1,POC,POC_Dummy],r"""1""", power_ppc)
        psspy.voltage_channel([-1,-1,-1,Inv], v_inv)
        psspy.machine_array_channel([-1,2,Inv],r"""1""",power_inv[0])
        psspy.machine_array_channel([-1,3,Inv],r"""1""",power_inv[1])   
        if Inv2 > 0:
            psspy.voltage_channel([-1,-1,-1,Inv2], v_inv2)
            psspy.machine_array_channel([-1,2,Inv2],r"""1""",power_inv2[0])
            psspy.machine_array_channel([-1,3,Inv2],r"""1""",power_inv2[1]) 


        #psspy.lines_per_page_one_device(1,60)
        psspy.change_channel_out_file(parent_dir + "\\outputs\\{}\\".format(proj) + outputname)
        #psspy.report_output(2,"",[0,0])
        ierr = psspy.set_netfrq(1)
        psspy.set_chnfil_type(0)
        psspy.strt(1,parent_dir + "\\outputs\\{}\\".format(proj) + outputname)
        psspy.snap([-1,-1,-1,-1,-1],snp_file)
        psspy.run(0,0.0,1,1,1)
        psspy.run(0,RUN_Time,1,1,1)
        psspy.prompt_output(2,"",[0,0])
        psspy.alert_output(2,"",[0,0])
        psspy.progress_output(2,"",[0,0])
        psspy.pssehalt_2()
        os.chdir(parent_dir)
    except:
        logerror()      
    return outputname, v_plot
    
def RunDynamics_FAULT(FRT,DisDur_Time,RUN_Time, FRT_X, Final_Time, z_sys, Sbase):
    try:
        import os,sys
        # PSSE_LOCATION = r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27"
        # sys.path.append(PSSE_LOCATION)
        # os.environ['PATH'] = os.environ['PATH'] + ';' +  r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN"
        import psse34
        import psspy
        import redirect
        parent_dir = os.getcwd()
        os.chdir('models/{}'.format(proj))
        if proj == 'PLSF':
            sav_file = 'PLSF_PE.sav'
            sav_cnv_file = 'PLSF_PE_cnv.sav'
            dyr_file = 'PLSF_PE_H1006D_Syncon.dyr'
            snp_file = 'PLSF_PE.snp'
            dll_file1 = 'PE_v34_2_H1006D.dll'
            dll_file2 = None#'SG3400HV_V28B10.dll'
            POC = 1150
            Inv = 1180
            Inv2 = 1181
            SIMB = 1130
            POC_Dummy = 1140
            K_POC = 132.0 
        elif proj == 'SGMODEL':
            sav_file = 'PASF_SMIB.sav'
            sav_cnv_file = 'PASF_SMIB_cnv.sav'
            dyr_file = 'PASF_SMIB.dyr'
            snp_file = 'PASF_SMIB.snp'
            dll_file1 = 'SG3400HV_V28B10.dll'
            dll_file2 = 'INACES-V28.0.dll'
            POC = 1011
            Inv = 1
            Inv2 = -1#1181
            SIMB = 1000
            POC_Dummy = 1000
            K_POC = 132.0 
        else:
            raise("wrong proj name")

        if FRT != 0:
            z_fault = complex(z_sys[0], z_sys[1])
            r_fault = (FRT /(1 -  FRT) * z_fault).real#*132*132/Sbase
            x_fault = (FRT /(1 -  FRT) * z_fault).imag#*132*132/Sbase
            g_fault = (1.0/(FRT /(1 -  FRT) * z_fault)).real
            b_fault = (1.0/(FRT /(1 -  FRT) * z_fault)).imag

            print(FRT)
            print(r_fault, x_fault)
            print(g_fault*Sbase, b_fault*Sbase)
            print(z_fault)
        else:
            r_fault = 0.0
            x_fault = 0.0
            g_fault = 0.0
            b_fault = -9999.0

        redirect.reset()
        redirect.psse2py()
        _i=psspy.getdefaultint()
        _f=psspy.getdefaultreal()
        _s=psspy.getdefaultchar()
        psspy.psseinit()
        outputname=now +'_'+ '5.2.5.4'+'_['+str(FRT)+']_['+ str(DisDur_Time)+']'+  '.out'
        recdFN=now +'_'+ '5.2.5.4'+'_['+str(FRT)+']_['+ str(DisDur_Time)+']'+'.recd'
        #psspy.lines_per_page_one_device(1,60)
        psspy.progress_output(2,parent_dir + "\\outputs\\{}\\".format(proj) + recdFN,[0,0])
        # psspy.lines_per_page_one_device(1,60)
        psspy.prompt_output(2,parent_dir + "\\outputs\\{}\\".format(proj) + recdFN,[0,0])
        #psspy.lines_per_page_one_device(1,60)
        psspy.alert_output(2,parent_dir + "\\outputs\\{}\\".format(proj) + recdFN,[0,0])
        #psspy.addmodellibrary(r"""GMD0352_v34.dll""")
        #psspy.addmodellibrary(r"""GC0520T_v34.dll""")
        #psspy.case(r"""BGWF_Gamesa_SMIB_R6_FRT.sav""")
        psspy.addmodellibrary(dll_file1)
        if dll_file2 != None:
            psspy.addmodellibrary(dll_file2)
        # print(sav_file)
        # raise
        psspy.case(sav_file)
        psspy.solution_parameters_4([_i,99,_i,_i,_i],[_f,_f,_f,_f,_f, 1e-05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f, 1e-05,_f,_f])
        psspy.fnsl([0,0,0,0,0,0,99,0])
        psspy.cong(0)
        psspy.conl(0,1,1,[0,0],[ 100.0,0.0,0.0, 100.0])
        psspy.conl(0,1,2,[0,0],[ 100.0,0.0,0.0, 100.0])
        psspy.conl(0,1,3,[0,0],[ 100.0,0.0,0.0, 100.0])
        psspy.ordr(0)
        psspy.fact()
        psspy.tysl(0)
        psspy.save(sav_cnv_file)
        psspy.dyre_new([1,1,1,1],dyr_file,r"""CONEC.flx""",r"""CONET.flx""","")
        psspy.dynamics_solution_param_2([1000,_i,_i,_i,_i,_i,_i,_i],[0.1 ,1e-06, 0.001,0.02,_f,_f,_f,_f])


        v_ppc = r"""V_POC_PASF"""
        v_inv = r"""V_PASF"""
        Edf_smib = r'SMIB_EDF'
        UUT_smib = r'SMIB_UUT'
        P_smib = r'SMIB_PELEC'
        Q_smib = r'SMIB_QELEC'
        power_inv = [r"""P_PASF""", r"""Q_PASF"""]
        power_ppc = [r"""P_POC_PASF""",r"""Q_POC_PASF"""]
        v_plot = {'POC Power Profile': [power_ppc, 'MW/MVAR'], 
                    'Inverter Power Profile': [power_inv, 'MW/MVAR'], 
                    'V int':[v_inv, 'p.u.'], 
                    'V ppc':[[v_ppc, UUT_smib, Edf_smib], 'p.u.'], 
                    'V SMIB':[Edf_smib, UUT_smib, 'p.u.'], 
                    'Power SMIB':[P_smib, Q_smib, 'p.u.'], }
        psspy.voltage_channel([-1,-1,-1,POC],v_ppc)
        if Inv2 > 0:
            v_inv = r"""V_PASF_{}""".format(Inv)
            v_inv2 = r"""V_PASF_{}""".format(Inv2)
            power_inv = [r"""P_PASF_{}""".format(Inv), r"""Q_PASF_{}""".format(Inv)]
            power_inv2 = [r"""P_PASF_{}""".format(Inv2), r"""Q_PASF_{}""".format(Inv2)]
            v_plot = {'POC Power Profile': [power_ppc, 'MW/MVAR'], 
                        'Inverter Power Profile @{}'.format(Inv): [power_inv, 'MW/MVAR'], 
                        'Inverter Power Profile @{}'.format(Inv2): [power_inv2, 'MW/MVAR'], 
                        'V int @{}'.format(Inv):[v_inv, 'p.u.'], 
                        'V int @{}'.format(Inv2):[v_inv2, 'p.u.'], 
                        'V ppc':[[v_ppc, UUT_smib, Edf_smib], 'p.u.'],
                        'Efd SMIB':[Edf_smib, 'p.u.'], 
                        'Power SMIB':[P_smib, Q_smib, 'p.u.'], }
        print(v_plot)
        psspy.voltage_channel([-1,-1,-1,POC],v_ppc)
        psspy.machine_array_channel([-1,5,SIMB],r"""1""", Edf_smib) 
        psspy.machine_array_channel([-1,4,SIMB],r"""1""", UUT_smib) 
        psspy.machine_array_channel([-1,3,SIMB],r"""1""", Q_smib)
        psspy.machine_array_channel([-1,2,SIMB],r"""1""", P_smib)
        psspy.branch_p_and_q_channel([-1,-1,-1,POC,POC_Dummy],r"""1""", power_ppc)
        psspy.voltage_channel([-1,-1,-1,Inv], v_inv)
        psspy.machine_array_channel([-1,2,Inv],r"""1""",power_inv[0])
        psspy.machine_array_channel([-1,3,Inv],r"""1""",power_inv[1])   
        if Inv2 > 0:
            psspy.voltage_channel([-1,-1,-1,Inv2], v_inv2)
            psspy.machine_array_channel([-1,2,Inv2],r"""1""",power_inv2[0])
            psspy.machine_array_channel([-1,3,Inv2],r"""1""",power_inv2[1]) 


        #psspy.lines_per_page_one_device(1,60)
        psspy.change_channel_out_file(parent_dir + "\\outputs\\{}\\".format(proj) + outputname)
        #psspy.report_output(2,"",[0,0])
        ierr = psspy.set_netfrq(1)

        psspy.set_chnfil_type(0)
        psspy.strt(1,parent_dir + "\\outputs\\{}\\".format(proj) + outputname)
        psspy.snap([-1,-1,-1,-1,-1],snp_file)
        psspy.run(0,0.0,1,1,1)
        psspy.run(0,RUN_Time,1,1,1)
        flg = 0
        if flg:
            psspy.dist_bus_fault(POC_Dummy,1, K_POC,[g_fault*Sbase, b_fault*Sbase])
        else:
            psspy.dist_bus_fault(POC_Dummy, 3, K_POC,[0,x_fault*K_POC*K_POC/Sbase])#r_fault*132*132/Sbase, 
            #psspy.dist_bus_fault(1011,3, 132.0,[r_fault*132*132/Sbase, x_fault*132*132/Sbase])
        # psspy.dist_bus_fault(1011,1, 132.0,[r_fault*132*132/100, x_fault*132*132/100])
        #psspy.dist_bus_fault(1011,1, 132.0,[0, (0.169/63.7+0.08/65+0.12/110)*132*132/100])
        #psspy.dist_bus_fault(1011,1, 132.0,[-126.3, 2.853])

        # balance the load
        flg = 0
        if flg:
            psspy.dist_bus_fault(POC,1, 132.0,[-132.20, 5.710]*(1))
        #psspy.dist_bus_fault(1011,1, 132.0,[g_fault*Sbase, b_fault*Sbase])
        #psspy.dist_bus_fault(1011,1, 132.0,[0,FRT_X])
        psspy.run(0, RUN_Time+DisDur_Time,5,1,0)
        psspy.dist_clear_fault(1)
        print('*'*10)
        psspy.run(0, Final_Time,5,1,0)
        

        psspy.prompt_output(2,"",[0,0])
        psspy.alert_output(2,"",[0,0])
        psspy.progress_output(2,"",[0,0])
        psspy.pssehalt_2()
        os.chdir(parent_dir)
    except:
        logerror()      
    return outputname, v_plot

def  writePLBFile(FRT,DisDur_Time, proj):           
    try:
        import os
        plbFile = open('models\\{}\\zingen1.plb'.format(proj),'w')
        plbFile.write('0,1,50\n')
        plbFile.write('10.999,1,50\n')
        plbFile.write('11,'+str(FRT)+',50\n')
        plbFile.write(str(DisStart_Time+DisDur_Time)+','+ str(FRT)+',50\n')
        plbFile.write(str(DisStart_Time+DisDur_Time+0.001)+',1,50\n')
        plbFile.write('22.0,1,50\n')
        plbFile.write('30.02,1,50\n')
        plbFile.close()     
    except:
        logerror()   
       
        
if __name__ == '__main__':
    proj = 'PLSF'#'SGMODEL'#
    flg_clean = 1
    if flg_clean:
        cleanUp(proj)

    flg = 0
    if flg:
        FRT =         [0,0.25,0.5,0.8]#, 1.225, 1.2, 1.118, 1.1, 0.9, 0.8, 0.7, 0.3]#Voltage disturbance at connection point
        DisDur_Time   = [0.43,0.43,0.43,10]#,   0.2, 0.4,   0.9,  10,  10,   1,   2, 0.5]#Disturbance duration 
        # FRT =         [0.8, 1.1]#, 1.225, 1.2, 1.118, 1.1, 0.9, 0.8, 0.7, 0.3]#Voltage disturbance at connection point
        # DisDur_Time   = [10, 10]#,   0.2, 0.4,   0.9,  10,  10,   1,   2, 0.5]#Disturbance duration 
        DisStart_Time = 11
        RUN_Time = 30
        for i in range(len(FRT)):
            outputname='5.2.5.4'+'_['+str(FRT[i])+']_['+ str(DisDur_Time[i]) +']_'+'.out'
            writePLBFile(FRT[i],DisDur_Time[i], proj) 
            outputname, v_plot = RunDynamics_PLB(FRT[i],DisDur_Time[i],RUN_Time, proj)
            #outputname, v_plot = RunDynamics_FAULT(FRT[i],DisDur_Time[i],RUN_Time,FRT_X[i],Final_Time, z_sys[j], Sbase)
            dynamic_plot_custom("outputs\\{}\\".format(proj) + outputname)

    else:
        z_sys = [[0.025100, 0.202600]]
        Sbase = 100
        Final_Time    = 30
        DisStart_Time = 5 # not used yet. cory
        RUN_Time = 5
        FRT =           [0,0.25,0.5,0.8]        #Voltage disturbance at connection point
        DisDur_Time   = [0.43,0.43,0.43,10]     #Disturbance duration 
        FRT_X         = [-99999,-2700,-900,-130]  # fault MVAr

        for j in range(len(z_sys)):
            for i in range(len(FRT)):
                outputname='5.2.5.4'+'_['+str(FRT[i])+']_['+ str(DisDur_Time[i]) +']_'+'.out'
                writePLBFile(FRT[i],DisDur_Time[i], proj) 
                #outputname, v_plot = RunDynamics_PLB(FRT[i],DisDur_Time[i],RUN_Time, proj)
                outputname, v_plot = RunDynamics_FAULT(FRT[i],DisDur_Time[i],RUN_Time,FRT_X[i],Final_Time, z_sys[j], Sbase)
                dynamic_plot_custom("outputs\\{}\\".format(proj) + outputname)
    
    csv_files = glob.glob("outputs\\{}\\".format(proj)+ "*.csv")
    pplot(csv_files, v_plot, proj)