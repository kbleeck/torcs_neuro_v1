#!/usr/bin/env python

import os
import subprocess
import glob
import xml.etree.ElementTree as ET
import GA
import signal
import time
import csv
import random
import logging
import operator
import shutil
import glob
import pprocess
EPSILON = 0.000001

def evaluation(parameters, ind):
    # Evaluation function is passed to the GA
    # Takes phenotype as parameters and port_id (=individual id, int) for parallel processing
    fullpath = os.path.abspath(".")
    port = 3000 + ind + 1
    guiless = 1
    if (guiless == 1):
        server = subprocess.Popen(["torcs", "-t 1000000000", "-r", fullpath + "/configs/" + str(port) + ".xml"])
    else:
        server = subprocess.Popen(["torcs",  fullpath + "/configs/" + str(port) + ".xml"])
    call_agent = ["python", "snakeoil.py"]
    port = ["-p", str(port)]
    parameters = map(str, parameters)
    call_agent.extend(port)
    call_agent.extend(parameters)
    subprocess.check_call(call_agent) #1
    subprocess.check_call(call_agent) #2
    subprocess.check_call(call_agent) #3
    subprocess.check_call(call_agent) #4
    subprocess.check_call(call_agent) #5
    subprocess.check_call(call_agent) #6
    subprocess.check_call(call_agent) #7
    subprocess.check_call(call_agent) #8
    subprocess.check_call(call_agent) #9
    subprocess.check_call(call_agent) #10
    server.kill() #1
    server.kill() #2
    server.kill() #3
    server.kill() #4
    server.kill() #5
    server.kill() #6
    server.kill() #7
    server.kill() #8
    server.kill() #9
    server.kill() #10
    # Gather data and parse
    result_file = "/home/max/.torcs/results/"+ str(port[1]) +"/*.xml"
    newest = max(glob.iglob(result_file), key = os.path.getctime)
    tree = ET.parse(newest)
    root = tree.getroot()
    races = [2,4,5,6,7,8,9,10,11,12]
    placing = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    for race in range(10):
        for place in range(2):
            if root[races[race]][1][0][1][place][0].attrib.get("val") in ("scr_server 1", "scr_server 2", "scr_server 3", "scr_server 4", "scr_server 5", "scr_server 6", "scr_server 7", "scr_server 8", "scr_server 9", "scr_server 10", "scr_server 11"):
               placing[race] = place
    for i in range(0, 9):
        print i
    laps1 = root[2][1][0][1][placing[0]][3].attrib.get("val")
    laps2 = root[4][1][0][1][placing[1]][3].attrib.get("val")
    laps3 = root[5][1][0][1][placing[2]][3].attrib.get("val")
    laps4 = root[6][1][0][1][placing[3]][3].attrib.get("val")
    laps5 = root[7][1][0][1][placing[4]][3].attrib.get("val")
    laps6 = root[8][1][0][1][placing[5]][3].attrib.get("val")
    laps7 = root[9][1][0][1][placing[6]][3].attrib.get("val")
    laps8 = root[10][1][0][1][placing[7]][3].attrib.get("val")
    laps9 = root[11][1][0][1][placing[8]][3].attrib.get("val")
    laps10 = root[12][1][0][1][placing[9]][3].attrib.get("val")
    time1 = root[2][1][0][1][placing[0]][4].attrib.get("val")
    time2 = root[4][1][0][1][placing[1]][4].attrib.get("val")
    time3 = root[5][1][0][1][placing[2]][4].attrib.get("val")
    time4 = root[6][1][0][1][placing[3]][4].attrib.get("val")
    time5 = root[7][1][0][1][placing[4]][4].attrib.get("val")
    time6 = root[8][1][0][1][placing[5]][4].attrib.get("val")
    time7 = root[9][1][0][1][placing[6]][4].attrib.get("val")
    time8 = root[10][1][0][1][placing[7]][4].attrib.get("val")
    time9 = root[11][1][0][1][placing[8]][4].attrib.get("val")
    time10 = root[12][1][0][1][placing[9]][4].attrib.get("val")
    penalty_time1 = root[2][1][0][1][placing[0]][5].attrib.get("val")
    penalty_time2 = root[4][1][0][1][placing[1]][5].attrib.get("val")
    penalty_time3 = root[5][1][0][1][placing[2]][5].attrib.get("val")
    penalty_time4 = root[6][1][0][1][placing[3]][5].attrib.get("val")
    penalty_time5 = root[7][1][0][1][placing[4]][5].attrib.get("val")
    penalty_time6 = root[8][1][0][1][placing[5]][5].attrib.get("val")
    penalty_time7 = root[9][1][0][1][placing[6]][5].attrib.get("val")
    penalty_time8 = root[10][1][0][1][placing[7]][5].attrib.get("val")
    penalty_time9 = root[11][1][0][1][placing[8]][5].attrib.get("val")
    penalty_time10 = root[12][1][0][1][placing[9]][5].attrib.get("val")
    damage1=root[2][1][0][1][placing[0]][8].attrib.get("val")
    damage2=root[4][1][0][1][placing[1]][8].attrib.get("val")
    damage3=root[5][1][0][1][placing[2]][8].attrib.get("val")
    damage4=root[6][1][0][1][placing[3]][8].attrib.get("val")
    damage5=root[7][1][0][1][placing[4]][8].attrib.get("val")
    damage6=root[8][1][0][1][placing[5]][8].attrib.get("val")
    damage7=root[9][1][0][1][placing[6]][8].attrib.get("val")
    damage8=root[10][1][0][1][placing[7]][8].attrib.get("val")
    damage9=root[11][1][0][1][placing[8]][8].attrib.get("val")
    damage10=root[12][1][0][1][placing[9]][8].attrib.get("val")
    p1=abs(float(time1) - float(penalty_time1) > EPSILON)
    p2=abs(float(time2) - float(penalty_time2) > EPSILON)
    p3=abs(float(time3) - float(penalty_time3) > EPSILON)
    p4=abs(float(time4) - float(penalty_time4) > EPSILON)
    p5=abs(float(time5) - float(penalty_time5) > EPSILON)
    p6=abs(float(time6) - float(penalty_time6) > EPSILON)
    p7=abs(float(time7) - float(penalty_time7) > EPSILON)
    p8=abs(float(time8) - float(penalty_time8) > EPSILON)
    p9=abs(float(time9) - float(penalty_time9) > EPSILON)
    p10=abs(float(time10) - float(penalty_time10) > EPSILON)
    print "total:"+str(float(time1)+float(time2)+float(time3)+float(time4)+float(time5)+float(time6)+float(time7)+float(time8)+float(time9)+float(time10))+"time1: "+str(time1)+" time2: "+str(time2)+" time3: "+str(time3)+" time4: "+str(time4)+" time5: "+str(time5)+" time6: "+str(time6)+" time7: "+str(time7)+" time8: "+str(time8)+" time9: "+str(time9)+" time10: "+str(time10)+" parameters: "+str(parameters)
    # Check whether the lap was actually finished and verify lap time
    #if laps > 0 and (float(time) - float(best_lap_time) < EPSILON):
    if (float(damage1)<10000.0) and  (float(damage2)<10000.0) and  (float(damage3)<10000.0) and (float(damage4) < 10000.0) and (float(damage5) < 10000.0) and (float(damage6)<10000.0) and (float(damage7)<10000.0) and (float(damage8)<10000.0)and (float(damage9)<10000.0)and (float(damage10)<10000.0):
        if float(time1)==0.0 or float(time2)==0.0or float(time3)==0.0:
            time = -1
        elif (laps1 > 0 and laps2 > 0 and laps3 > 0 and laps4 > 0 and laps5 > 0 and laps6 > 0 and laps7 > 0 and laps8 > 0 and laps9 > 0 and laps10 > 0 and p1 and p2 and p3 and p4 and p5 and p6 and p7 and p8 and p9 and p10 and (float(time1)> 40.0) and (float(time2)> 40.0) and (float(time3)> 40.0) and (float(time4)> 40.0) and (float(time5)> 40.0) and (float(time6)> 40.0) and (float(time7)> 40.0) and (float(time8)> 40.0) and (float(time9)> 40.0) and (float(time10)> 40.0)):
           time = float(time1)+float(time2)+float(time3)+float(time4)+float(time5)+float(time6)+float(time7)+float(time8)+float(time9)+float(time10)
           #print "now timeX: "+str(time)
        else:
            time = -1
    else:
        time=-1
        print "to much damage. track 1: "+str(float(root[2][1][0][1][placing[0]][8].attrib.get("val")))
        print "to much damage. track 2: "+str(float(root[4][1][0][1][placing[0]][8].attrib.get("val")))
    return time

def main():
    rep_length = 14
    popsize =12
    sp = 3
    mut = 1./rep_length
    cross = 0.95
    maxgen = 100
    onlyThebest = 0
    run_id = "1"
    nr_processes = 6
    fullpath = os.path.abspath(".")
    for runval in range(39, 1000):
        print "run "+str(runval)
        optimizer = GA.gax(rep_length = rep_length, popsize = popsize, sp = sp, mut = mut, fitfun = evaluation, maxgen = maxgen, cross = cross, nr_processes = nr_processes, run_id = run_id, path = fullpath,onlyThebest=onlyThebest, runval=runval)
        optimizer.run()
        bashCommand = "killall torcs-bin"
        os.system(bashCommand)
        print "killed old torcs processes"

if __name__ == "__main__":
    main()
