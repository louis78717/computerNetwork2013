import subprocess

from datetime import datetime # Used the genreate the filename
f = open('myfile','w')

while True:
    fileName = str(datetime.now().day) + "-" + str(datetime.now().month) + "-" + str(datetime.now().year) + " AT " + str(datetime.now().hour) + "-" + str(datetime.now().minute)
    tcpDumpProcess = subprocess.Popen(["tcpdump", "-Z", "root", "-w", fileName, "-i", "bridge0", "-G", "60", "-W", "1"]) #Sets up the TCPDump command
    tcpDumpProcess.communicate() #Runs the TCPDump command
    print(fileName) #Uploads the dump file to dropbox
    f.write(fileName+'\n')
    #print "File uploaded Successfully"