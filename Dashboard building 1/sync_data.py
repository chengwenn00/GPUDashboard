import csv, os
import subprocess
with open('./hostnames.csv', 'r') as read_obj:
    csv_reader = csv.reader(name)
    for host_array in csv_reader:
        host = host[0]
        path = './{}/'.format(host)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print("The new directory is created!")

        if host_array[1]=="Linux":
            # cmd = add own command
            process = subprocess.Popen(cmd)
            cmd = 
            process = subprocess.Popen(cmd)

        elif host_array[1]=="Linux_old":
            cmd 
            process = subprocess.Popen(cmd)
        else:
            cmd 
            process = subprocess.Popen(cmd)
            cmd 
            process = subprocess.Popen(cmd)



        
