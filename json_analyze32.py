import requests
import json
import re
import time
import datetime
import sys
import os


final_array = []
pilot_array = []
file_array  = []
start_time = 1543110628
host_name = ""

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

def print_key_value(K,V):
    for k in range(len(K)):
        print ("key = ", K[k] ,"      ","value = ", V[k],"   \n ")
    
def lt(epoch_time):
    #return(datetime.datetime.fromtimestamp(epoch_time).strftime('%c'))
    return(datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S'))


def AccountingGroup_p(a):
    #print(a)
    L= len(a)
    b= [True]*len(a)

    for i in range(len(a)):
        if "production" in a[i]:
            b[i] = True
        else:
            b[i] = False
    return(b)                                                                                                                                               

#def total(accountingGroup,ChildMemory,ChildCpus,retiret,dietime,prod,name):
def total(Gliden_id,ChildMemory,ChildCpus,file_index,retiret,dietime,prod,name):
    global pilot_array 
    global file_array 
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
     
    #print (bcolors.CGREEN2  , "{0:30s}  {1:12s}".format(Gliden_id,name),bcolors.OKGREEN + "  {0:<6d}     {1:<6d}".format(sumMem_P,sumCpu_P),\
    #bcolors.OKBLUE + "{0:<6d}     {1:<6d}".format(sumMem_A,sumCpu_A) + bcolors.CYELLOW2+" {0:<6d}     {1:<6d} ".format(sumMem_A+sumMem_P,sumCpu_A+sumCpu_P)\
    # + bcolors.ENDC + "{0:<10d}    {1:<5d} ".format(dietime,round((dietime-start_time)/3600)) + bcolors.ENDC )

    print("{0:25s} {1:12s}".format(Gliden_id,name), "  {0:<6d}     {1:<6d}".format(sumMem_P,sumCpu_P),\
     "{0:<6d}     {1:<6d}".format(sumMem_A,sumCpu_A) ," {0:<6d}     {1:<6d} ".format(sumMem_A+sumMem_P,sumCpu_A+sumCpu_P)\
     , "{0:<10d}    {1:<5d}   {2:<5d}".format(dietime,round((dietime-start_time)/3600),round((int(file_index)-1000)/6)))

    #print("I am at pilot_arry inside inside :",pilot_array)
    for i in range(len(pilot_array)):
        if Gliden_id in pilot_array[i]:
            print("{0:25s} {1:12s}".format(Gliden_id,name), "  {0:<6d}     {1:<6d}".format(sumMem_P,sumCpu_P),"{0:<6d}     {1:<6d}".format(sumMem_A,sumCpu_A)\
             ," {0:<6d}     {1:<6d} ".format(sumMem_A+sumMem_P,sumCpu_A+sumCpu_P), "{0:<10d}    {1:<5d}   {2:<5d}".format(dietime,round((dietime-start_time)/3600)\
                ,round((int(file_index)-1000)/6)),file=file_array[i])    
     


def analysis(accountingGroup,ChildMemory,ChildCpus,prod,name):
    #print (type(prod),len(prod))
    L = len(prod)
    sumMem = 0
    sumCpu = 0
    for i in range(L):
        if not prod[i]:
            sumMem += ChildMemory[i]
            sumCpu += ChildCpus[i]
            #print(accountingGroup[i],"  ",ChildMemory[i],"   ",ChildCpus[i])
            #print("  ",ChildMemory[i],"   ",ChildCpus[i])
    if sumCpu:
        print (name,"   ",sumMem,"           ",sumCpu,"              ",1.*sumMem/sumCpu)



def production(accountingGroup,ChildMemory,ChildCpus,prod,name):
    #print (type(prod),len(prod))
    L = len(prod)
    sumMem = 0
    sumCpu = 0
    for i in range(L):
        if prod[i]:
            sumMem += ChildMemory[i]
            sumCpu += ChildCpus[i]
            #print(accountingGroup[i],"  ",ChildMemory[i],"   ",ChildCpus[i])
            #print("  ",ChildMemory[i],"   ",ChildCpus[i])
    if sumCpu:
        print (name,"   ",sumMem,"           ",sumCpu,"              ",1.*sumMem/sumCpu)

def make_gnuplot_file():
    global pilot_array 
    global file_array 
    str_file_total_mem = 'plot '
    str_file_total_cpu = 'plot '
    for i in range(len(pilot_array)):
        str_file_total_mem += '"'
        str_file_total_mem += str(file_array[i].name)
        str_file_total_mem += '"'
        #str_file_total_mem += ' u 11:7 w  point pointtype '+ str(i) +',' 
        str_file_total_mem += ' u 11:7 w l ,' 
        str_file_total_cpu += '"'
        str_file_total_cpu += str(file_array[i].name)
        str_file_total_cpu += '"'
        #str_file_total_cpu += ' u 11:8 w point pointtype '  + str(i)+','
        str_file_total_cpu += ' u 11:8 w l ,' 


    print(str_file_total_mem,'\n',str_file_total_cpu)

    

def printout_this(a,hostname):
    global pilot_array 
    global file_array 
    for file in range(len(pilot_array)):
        #print(file,pilot_array[file])
        fname = hostname+'-'+pilot_array[file]
        #ff = open(fname,"w")
        file_array.append(open(fname,"w"))
        #print("hi",file=file_array[file])
        #print("-------------------->",fname)

    for i in range(len(a)):
        #print(a[i][0],"  ",round((int(a[i][7])-start_time)/3600)," ",round((int(a[i][8])-start_time)/3600),"\n")
        #print(a[i],"\n")
        
        Gliden_id = a[i][0]
        file_index = a[i][2]
        ChildMemory = a[i][3]
        ChildCpus = a[i][4]
        ChildAccountingGroup = a[i][6]
        Total_Memory_left = a[i][7]
        RetireTime = a[i][8]
        DieTime = a[i][9]
        TotalMemory_requested = a[i][10] 
        Total_Cpus_left = a[i][11]
        TotalSlotCpus_Requested = a[i][12] 
        prod = AccountingGroup_p(ChildAccountingGroup)
        #print(prod,"\n" ,ChildAccountingGroup,"\n")
        if ((int(DieTime)-int(RetireTime))) == 14400 and Gliden_id in pilot_array:
            total(Gliden_id,ChildMemory,ChildCpus,file_index,RetireTime,DieTime,prod,hostname)


def giveme_non_empty(dic):
    HT_nodes  = ["hammer-a004","hammer-a005","hammer-a006","hammer-a007","hammer-a008","hammer-a009","hammer-a010","hammer-a011","hammer-a012","hammer-a013",\
    "hammer-b","hammer-c","hammer-d"]
    global host_name
    dic1 = {}
    for key,value in dic.items():
            #print("I am at key,value:   ",key,value)
            if len(value) > 0:
                if host_name[:8]  in HT_nodes or host_name in HT_nodes:
                    #print ("I am at value-2:  ",value[-2:])
                    dic1[key] = value[-2:]
                else:
                    dic1[key] = value[-1:]

    print("I am at dic1    ",dic1,host_name,"\n\n")
    return(dic1)
     



def giveme_values_array(dic):
    just_values = []
    for item in dic.values():
            #print("I am at item:   ",item)
            just_values += item
    #print(just_values)
    return just_values

def exclude_dead_pilot(pilot_b):
    global start_time
    pilot_number = {}
    for p in pilot_b:
        #print(p,"\n")
        if p[0] not in pilot_number:
            pilot_number[p[0]] = 1
        else:
            pilot_number[p[0]] += 1
    #for pp in   pilot_number.items():
        #print("how many ",pp)      
    pilot_and_retiretime = list(set(pilot_b))
    #for p in pilot_and_retiretime:
     #   print(p)

    pilot_and_retiretime_sorted =  sorted(pilot_and_retiretime, key=lambda x:x[1])
    #for p in pilot_and_retiretime_sorted:
        #print(p)

    delta_t = [0]
    for i in  range(0,len(pilot_and_retiretime_sorted)-1):
        delta_t.append( pilot_and_retiretime_sorted[i+1][1]-pilot_and_retiretime_sorted[i][1])
    sum_delta = 0    
    for i in range(0,len(pilot_and_retiretime_sorted)):
         #print(pilot_and_retiretime_sorted[i][0],"   ",pilot_and_retiretime_sorted[i][1],"  ",delta_t[i],"  ",int(delta_t[i]/3600.))
         sum_delta += delta_t[i]
         print("{0:3d}   {1:<30s}   {2:<15d}  {3:<10d}  {4:<5d}  {5:<5d}   {6:<5d}  {7:<10d}".format(i,    pilot_and_retiretime_sorted[i][0],pilot_and_retiretime_sorted[i][1],\
        delta_t[i],int(delta_t[i]/3600.),int(sum_delta/3600.),pilot_number[pilot_and_retiretime_sorted[i][0]],\
        int((pilot_and_retiretime_sorted[i][1]-start_time)/3600.)))

    #selected_pilot = {}
    selected_pilot = {k: [] for k in range(len(pilot_and_retiretime_sorted))}
    #print(selected_pilot,"\n\n")
    count  = 0
    for j  in range(len(pilot_and_retiretime_sorted)):
        if pilot_and_retiretime_sorted[j][0] not in giveme_values_array(selected_pilot) and pilot_number[pilot_and_retiretime_sorted[j][0]] > 3:
            selected_pilot[count].append(pilot_and_retiretime_sorted[j][0])
            #print(pilot_and_retiretime_sorted[j][0],"    ",selected_pilot,"\n")
            for i in range(j+1,len(pilot_and_retiretime_sorted)):
                delta_time = pilot_and_retiretime_sorted[i][1] - pilot_and_retiretime_sorted[j][1]
                ##################### here is arbitrary numberts 5 and 40 could be very important 
                if delta_time < 5*3600 and pilot_number[pilot_and_retiretime_sorted[i][0]] > 3:          # 10 hours
                    selected_pilot[count].append( pilot_and_retiretime_sorted[i][0])
            count += 1
    #print("I am at selected pilot:  ",selected_pilot,"\n") 
    select_final_pilot = giveme_non_empty(selected_pilot)
    print("I am at final selected ",select_final_pilot,"\n\n")

    #print(giveme_values_array(selected_pilot))
    return giveme_values_array(select_final_pilot)
    
        

        

def do_all_for_this_hostname(hostname):
    global pilot_array
    pilot_a =[]
    pilot_b =[]
    all_pilot_for_this_hostname_not_sorted =[]
    all_pilot_for_this_hostname_sorted =[]
    for pilot in final_array:
        #print("IiiiiIiiiIIIIiIIIiIIIIIiIIIIIIIIII",pilot[9],pilot[8],pilot[9]-pilot[8])
        if hostname in pilot[1] and (pilot[9]-pilot[8] == 14400):
            #print("IiiiiIiiiIIIIiIIIiIIIIIiIIIIIIIIII",pilot[9],pilot[8],pilot[9]-pilot[8])
            pilot_a.append(pilot[0])
            #pilot_b.append((pilot[0],pilot[9]))
            #print(pilot)
            all_pilot_for_this_hostname_not_sorted.append(pilot)
    
    print("lennnnnnnnnnnn",len(all_pilot_for_this_hostname_not_sorted)) 
    
    
    all_pilot_for_this_hostname_sorted = sorted(all_pilot_for_this_hostname_not_sorted, key=lambda x:x[9])

    for ppp in all_pilot_for_this_hostname_sorted:
        pilot_b.append((ppp[0],ppp[9]))

    

    #####. Wxamining the array:
    time_0 = all_pilot_for_this_hostname_sorted[0][9]
    relative_time = []
    relative_time.append(0)
    time_pre = time_0
    time_post = 0
    '''
    for pp in all_pilot_for_this_hostname_sorted[1:]:
        print("I am here  ",pp[0],pp[8],pp[9],pp[9]-time_0,int((pp[9]-time_0)/3600))
        time_post = pp[9]
        relative_time.append(time_post-time_pre)
        time_pre = time_post
    #for i  in range(len(all_pilot_for_this_hostname_sorted[1:])):
    #    print("thisisdiff. ",all_pilot_for_this_hostname_sorted[i][0],"   ",relative_time[i])
    '''

    ####
    selected_pilot = exclude_dead_pilot(pilot_b)
    print("I am here inside:   ",selected_pilot)

    # here is a good place to comprae between nornal computation and uisng exclusion
    #pilot_array = list(set(pilot_a))
    pilot_array = exclude_dead_pilot(pilot_b)
    print("I am here at pilot_array",pilot_array)


    #pilot_array = set(pilot_a)

    printout_this(all_pilot_for_this_hostname_sorted,hostname) 
    #print(all_pilot_for_this_hostname_sorted)            
    make_gnuplot_file()

def main():
    global start_time
    global host_name

    #['http://localhost:8080/site_summary.1346', 'http://localhost:8080/site_summary.1681']# 
    url = "http://localhost:8080/all_hammer_jason_60_2000.json"
    first_file_command = "stat -s /usr/local/Cellar/nginx/1.15.6/html/site_summary.1000"
    res = os.popen(first_file_command).read().split()[11].split("=")[1]
    #print("I am here in start time",res)
    start_time = int(res)    
  
    result = requests.get(url)
    #host_name = "hammer-a008"
    host_name =  sys.argv[1]

   
    dataobj = result.json()
     
    #print(json.dumps(dataobj,indent=4))
    #print(dataobj.keys())
    for hostname in list(dataobj.keys()):
         
        data = dataobj[hostname]    
           
        for jason_pilot in data:
            pre_final_array = []
            #print(i,data[j],"\n",list(data[j].keys())," \n\n ",list(data[j].values())[0],"\n")
            #print(jason_pilot,"\n",list(jason_pilot.keys())[0],"\n\n",list(jason_pilot.values())[0],"\n\n\n")
            pilot_id = list(jason_pilot.keys())[0]
            #print(jason_pilot)

            temp_dic = list(jason_pilot.values())[0]
            pid_s = pilot_id.split("@") 
            #print(pid_s)
            pre_final_array.append(pid_s[1])
            pre_final_array.append(pid_s[2])
            pre_final_array.append(pid_s[3])
            for k in temp_dic.keys():
                #print(k,temp_dic[k],"\n",pre_final_array)
                #print(pre_final_array,"\n")
                pre_final_array.append(temp_dic[k])
            #print(pre_final_array,"\n")
            final_array.append(pre_final_array)
            #print("-------------------------------------\n\n\n")
    do_all_for_this_hostname(host_name)        
    
        

if __name__ == "__main__":
    main()
