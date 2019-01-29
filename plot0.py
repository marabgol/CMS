import requests
import json
import re
import time
import datetime
import os
import subprocess
import sys

hostname =''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CGREY    = '\033[90m'
    CRED2    = '\033[91m'
    CGREEN2  = '\033[92m'
    CYELLOW2 = '\033[93m'
    CBLUE2   = '\033[94m'
    CVIOLET2 = '\033[95m'
    CBEIGE2  = '\033[96m'
    CWHITE2  = '\033[97m'

 
def total(accountingGroup,ChildMemory,ChildCpus,retiret,dietime,prod,name,file_number,file_birthtime):
    L = len(prod)
    sumMem_A = 0
    sumCpu_A = 0
    sumMem_P = 0
    sumCpu_P = 0
    for i in range(L):
        if not prod[i]:
            sumMem_A += ChildMemory[i]
            sumCpu_A += ChildCpus[i]
        else:
            sumMem_P += ChildMemory[i]
            sumCpu_P += ChildCpus[i]
    #print (bcolors.HEADER + name, bcolors.OKGREEN + "Production   ",sumMem_P,"     ",sumCpu_P, \
    #bcolors.OKBLUE + "     Analysis         ",sumMem_A,"      ",sumCpu_A , bcolors.ENDC +" ")

    #print ( bcolors.HEADER  + "%12s" %(name),bcolors.OKGREEN + "Production   %10d   %10d "  %(sumMem_P,sumMem_P),bcolors.OKBLUE +   "  Analysis        %10d    %10d  " %  (sumMem_A,sumMem_A),bcolors.ENDC) 
    #print (bcolors.HEADER  + "%12s" %(name),bcolors.OKGREEN + "Production   {0:<6d}  {1:<6d}".format(sumMem_P,sumMem_P),bcolors.OKBLUE + "Production   {0:<6d}  {1:<6d}".format(sumMem_A,sumMem_A))
    print ( "%12s" %(name), "  {0:<6d}     {1:<6d}".format(sumMem_P,sumCpu_P), "{0:<6d}     {1:<6d}".format(sumMem_A,sumCpu_A) , " {0:<6d}     {1:<6d} ".format(sumMem_A+sumMem_P,sumCpu_A+sumCpu_P), "{0:<15d}    {1:<15d}    {2:<15d}  {3:<5d} ".format(lt(dietime),lt(retiret),file_birthtime,file_number ))
    print ( "%12s" %(name), "  {0:<6d}     {1:<6d}".format(sumMem_P,sumCpu_P), "{0:<6d}     {1:<6d}".format(sumMem_A,sumCpu_A) , " {0:<6d}     {1:<6d} ".format(sumMem_A+sumMem_P,sumCpu_A+sumCpu_P), "{0:<15d}    {1:<15d}    {2:<15d}  {3:<5d} ".format(lt(dietime),lt(retiret),file_birthtime,file_number ),file=out_file)
    # + "{0:<20s}   will die {3:<5d}s later ".format(lt(retiret),dietime-retiret) + bcolors.ENDC)
 
 
def find_range(dic_pilot):
    hours0 = []

    for pilot in dic_pilot.keys():
        for p in dic_pilot[pilot]:
            hours0.append(int(p[0]))
            #print(p)
    hours = list(set(hours0))        
    #print(hours,max(hours),hours[-1])
    return(hours[-1])
def make_gnuplot(dic_pilot):
        str_mem_prod = 'plot '
        str_cpu_prod = 'plot '
        str_mem_ana = 'plot '
        str_cpu_ana = 'plot '
        str_mem_all = 'plot '
        str_cpu_all = 'plot '
        for pilot in dic_pilot.keys():            
            str_mem_prod += "'"
            str_cpu_prod += "'"
            str_mem_prod += str(pilot)
            str_cpu_prod += str(pilot)
            str_mem_prod += "'"
            str_cpu_prod += "'"
            str_mem_prod += ' u 11:3 w l  lc 2 lw 2  title "production",'
            str_cpu_prod += ' u 11:4 w l lc 2 lw 2 title "production" ,'

            str_mem_ana += "'"
            str_cpu_ana += "'"
            str_mem_ana += str(pilot)
            str_cpu_ana += str(pilot)
            str_mem_ana += "'"
            str_cpu_ana += "'"
            str_mem_ana += ' u 11:5 w l lc 1 lw 1  title "Analysis",'
            str_cpu_ana += ' u 11:6 w l lc 1 lw 1 title "Analysis",'

            str_mem_all += "'"
            str_cpu_all += "'"
            str_mem_all += str(pilot)
            str_cpu_all += str(pilot)
            str_mem_all += "'"
            str_cpu_all += "'"
            str_mem_all += ' u 11:7 w l lc 4 lw 4 title "Total",'
            str_cpu_all += ' u 11:8 w l  lc 4 lw 4 title "Total",'

        print(str_mem_prod,"\n\n")
        print(str_cpu_prod,"\n\n")
        print(str_mem_ana,"\n\n")
        print(str_cpu_ana,"\n\n")
        print(str_mem_all,"\n\n")
        print(str_cpu_all,"\n\n")
        print(str_cpu_prod +str_cpu_ana[4:] +str_cpu_all[4:],"\n\n")
        print(str_mem_prod +str_mem_ana[4:] +str_mem_all[4:],"\n\n")



def commulative(dic_pilot,last_hour):
    sum_of_all = [[k,0,0,0,0] for k in range(last_hour)]
    #print(sum_of_all)
    
    for pilot in dic_pilot.keys():
        
        if (len(dic_pilot[pilot]) > 10     ):
            #print('Hi this length',len(dic_pilot[pilot]),dic_pilot[pilot])    
            for p in dic_pilot[pilot]:
                for i in range(last_hour):
                    if(int(p[0])) == i:
                        #print("Hiiiiiiii",p,i)
                        production_memory = int(p[1]) 
                        production_cpu = int(p[2]) 
                        analysis_memory = int(p[3]) 
                        analysis_cpu = int(p[4])
                        sum_of_all[i][1] += production_memory 
                        sum_of_all[i][2] += production_cpu
                        sum_of_all[i][3] += analysis_memory
                        sum_of_all[i][4] += analysis_cpu
    #print(sum_of_all)
    
    sum_of_all_file = open(hostname+'-sum.txt',"w")
    for i in range(last_hour):
        print("{0:4d}  {1:6d}  {2:2d}  {3:6d}  {4:2d}".format(sum_of_all[i][0],sum_of_all[i][1],sum_of_all[i][2],sum_of_all[i][3],sum_of_all[i][4]),file=sum_of_all_file)
    sum_of_all_gnu_mem = open(hostname+'_sum_mem.gn',"w")
    sum_of_all_gnu_cpu = open(hostname+'_sum_cpu.gn',"w")
    print('plot '+'"'+hostname+'-sum.txt'+'"'+ ' u 1:2 w l lc 2 lw 3  title "production",64000, '+'"'+hostname+'-sum.txt'+'"'+ ' u 1:4 w l lc 1 lw 2  title "Analysis",'+'"'+hostname+'-sum.txt'+'"'+ ' u 1:($2)+($4) w l lc 4 lw 4 title "Total"',file=sum_of_all_gnu_mem)
    print('plot '+'"'+hostname+'-sum.txt'+'"'+ ' u 1:3 w l lc 2 lw 3 title "production",20,40, '+'"'+hostname+'-sum.txt'+'"'+ ' u 1:5 w l lc 1 lw 2  title "Analysis",'+'"'+hostname+'-sum.txt'+'"'+ ' u 1:($3)+($5) w l lc 4 lw 4 title "Total"',file=sum_of_all_gnu_cpu)


def main():
    global hostname
    hostname =  sys.argv[1]
    files = os.popen("cd /Users/marabgol/Documents/gliden-summary ; ls " + hostname +"-glidein_*").read()
    #urls = os.popen("ls /usr/local/Cellar/nginx/1.15.6/html/site_summary.1???").read()
    #urls = subprocess.call(['ls' ,'/usr/local/Cellar/nginx/1.15.6/html/site_summary.* '])
    #print(urls,len(urls))
    array_pilot_name =[]
    array_pilot_file =[]
    files0 = files.split('\n')
    #print(files0)
    for s in files0:
        if len(s) >0:
            print(s)
            array_pilot_name.append(s)
    print(array_pilot_name)
    dic_for_each_pilot = {k: [] for k in array_pilot_name}  
    for file_name in array_pilot_name:
        array_pilot_file.append(open(file_name,'r'))
    for filename in array_pilot_file:
         
        for line in filename:
            tmp_line = []
            ll = line.split()
            tmp_line.append(ll[10])
            tmp_line.append(ll[2])
            tmp_line.append(ll[3])
            tmp_line.append(ll[4])
            tmp_line.append(ll[5])
            tmp_line.append(ll[8])
            tmp_line.append(ll[9])

            print(tmp_line)
            dic_for_each_pilot[filename.name].append(tmp_line)

    #for pilot in dic_for_each_pilot.keys():
    #    print(pilot,dic_for_each_pilot[pilot])
    #find_range(dic_for_each_pilot) 
    #print(dic_for_each_pilot)       
    make_gnuplot(dic_for_each_pilot)
    commulative(dic_for_each_pilot,find_range(dic_for_each_pilot))
       
    
if __name__ == "__main__":
    main()
