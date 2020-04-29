import subprocess
import sys,string,math,os
import ConfigParser
import glob
import numpy as np
from sampleAndMasses import *

filesPerList=100


def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)

if __name__ == "__main__":
    if Sample == 'TCP':
        for mass in masses:
            fileListDir="./filelists/TCP/"+mass+"/"
            checkAndMakeDir("./filelists/TCP/")
            checkAndMakeDir(fileListDir)
            clearDir(fileListDir)
            for job in range(1, 101): 
                filelistIdx=int((job-1)/filesPerList)
                if job%filesPerList==1:
                    out=open(fileListDir+"TCP_"+mass+"_"+str(filelistIdx)+".txt","w")
                out.write(prefix+"ALP_"+mass+"_w1_htjmin400_RunIISummer16DR80Premix_miniAODSIM_"+str(int(job))+".root\n")
                
    else:
        for mass in masses:
#            fileListDir="./filelists_LM/"+Sample+"/"+mass+"/"
#            checkAndMakeDir("./filelists_LM/"+Sample)
            fileListDir="./filelists/"+Sample+"/"+mass+"/"
            checkAndMakeDir("./filelists/"+Sample)
            checkAndMakeDir(fileListDir)
            clearDir(fileListDir)
            #print mass
            searchString=preSearchString.replace("REPLACEME",mass)
            os.system('dasgoclient --query "'+searchString+'"')
            query = 'dasgoclient --query "file dataset='+searchString+'"'
            files=os.popen(query).read().split()
            
            for nf in range(1, len(files)+1):
                filelistIdx=int((nf-1)/filesPerList)
                if nf%filesPerList==1:
                    out=open(fileListDir+Sample+"_"+mass+"_"+str(filelistIdx)+".txt","w")
                out.write(prefix+files[nf-1]+"\n")
            
