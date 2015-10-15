#!/usr/bin/env python

#TO DO: source cmssw grid env

import os,sys
import optparse
import commands
import time

#initialize t3 for submission
os.system('source /opt/exp_soft/cms//t3/t3setup')
if os.path.isfile("FailedJobs.txt") :
    os.system('rm FailedJobs.txt')
os.system('grep "End Fatal" log*.txt >>FailedJobs.txt')

failed = open("FailedJobs.txt","r")
for line in failed:
    words = line.split("_")
    os.system("rm log_{0}_job.txt".format(words[1]))
    os.system("/opt/exp_soft/cms/t3/t3submit -q cms \'runJob_%s.sh\'"%(words[1]))
    #print "/opt/exp_soft/cms/t3/t3submit -q cms \'runJob_%s.sh\'"%(words[1])
