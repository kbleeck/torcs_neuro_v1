#!/usr/bin/python
# snakeoil.py
# Chris X Edwards <snakeoil@xed.ch>
# Snake Oil is a Python library for interfacing with a TORCS
# race car simulator which has been patched with the server
# extentions used in the Simulated Car Racing competitions.
# http://scr.geccocompetitions.com/
#
# To use it, you must import it and create a "drive()" function.
# This will take care of option handling and server connecting, etc.
# To see how to write your own client do something like this which is
# a complete working client:
# /-----------------------------------------------\
# |#!/usr/bin/python                              |
# |import snakeoil                                |
# |if __name__ == "__main__":                     |
# |    C= snakeoil.Client()                       |
# |    for step in xrange(C.maxSteps,0,-1):       |
# |        C.get_servers_input()                  |
# |        snakeoil.drive_example(C)              |
# |        C.respond_to_server()                  |
# |    C.shutdown()                               |
# \-----------------------------------------------/
# This should then be a full featured client. The next step is to
# replace 'snakeoil.drive_example()' with your own. There is a
# dictionary which holds various option values (see `default_options`
# variable for all the details) but you probably only need a few
# things from it. Mainly the `trackname` and `stage` are important
# when developing a strategic bot. 
#
# This dictionary also contains a ServerState object
# (key=S) and a DriverAction object (key=R for response). This allows
# you to get at all the information sent by the server and to easily
# formulate your reply. These objects contain a member dictionary "d"
# (for data dictionary) which contain key value pairs based on the
# server's syntax. Therefore, you can read the following:
#    angle, curLapTime, damage, distFromStart, distRaced, focus,
#    fuel, gear, lastLapTime, opponents, racePos, rpm,
#    speedX, speedY, speedZ, track, trackPos, wheelSpinVel, z
# The syntax specifically would be something like:
#    X= o[S.d['tracPos']]
# And you can set the following:
#    accel, brake, clutch, gear, steer, focus, meta 
# The syntax is:  
#     o[R.d['steer']]= X
# Note that it is 'steer' and not 'steering' as described in the manual!
# All values should be sensible for their type, including lists being lists.
# See the SCR manual or http://xed.ch/help/torcs.html for details.
#
# If you just run the snakeoil.py base library itself it will implement a
# serviceable client with a demonstration drive function that is
# sufficient for getting around most tracks.
# Try `snakeoil.py --help` to get started.

import socket 
import sys
import getopt
PI= 3.14159265359

# Initialize help messages
ophelp=  'Options:\n'
ophelp+= ' --host, -H <host>    TORCS server host. [localhost]\n'
ophelp+= ' --port, -p <port>    TORCS port. [3001]\n'
ophelp+= ' --id, -i <id>        ID for server. [SCR]\n'
ophelp+= ' --steps, -m <#>      Maximum simulation steps. 1 sec ~ 50 steps. [100000]\n'
ophelp+= ' --episodes, -e <#>   Maximum learning episodes. [1]\n'
ophelp+= ' --track, -t <track>  Your name for this track. Used for learning. [unknown]\n'
ophelp+= ' --stage, -s <#>      0=warm up, 1=qualifying, 2=race, 3=unknown. [3]\n'
ophelp+= ' --debug, -d          Output full telemetry.\n'
ophelp+= ' --help, -h           Show this help.\n'
ophelp+= ' --version, -v        Show current version.'
usage= 'Usage: %s [ophelp [optargs]] \n' % sys.argv[0]
usage= usage + ophelp
version= "20130505-2"

class Client():
    def __init__(self):
        # If you don't like the option defaults,  change them here.
        self.host= 'localhost'
        self.port= 3002
        self.sid= 'SCR'
        self.maxEpisodes=1
        self.trackname= 'unknown'
        self.stage= 3
        self.debug= False
        self.maxSteps= 100000  # 50steps/second
        self.param = self.parse_the_command_line()
        self.S= ServerState()
        self.R= DriverAction()
        self.setup_connection()

    def setup_connection(self):
        # == Set Up UDP Socket ==
        try:
            self.so= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, emsg:
            #print("Error: Could not create socket...")
            sys.exit(-1)
        # == Initialize Connection To Server ==
        self.so.settimeout(1)
        while True:
            a= "-90 -75 -60 -45 -30 -20 -15 -10 -5 0 5 10 15 20 30 45 60 75 90"
            initmsg='%s(init %s)' % (self.sid,a)

            try:
                self.so.sendto(initmsg, (self.host, self.port))
            except socket.error, emsg:
                sys.exit(-1)
            sockdata= str()
            try:
                sockdata,addr= self.so.recvfrom(1024)
            except socket.error, emsg:
                #print("Waiting for server............")
                pass
            if '***identified***' in sockdata:
                #print("Client connected..............")
                break

    def parse_the_command_line(self):
        try:
            (opts, args) = getopt.getopt(sys.argv[1:], 'H:p:i:m:e:t:s:dhv',
                       ['host=','port=','id=','steps=',
                        'episodes=','track=','stage=',
                        'debug','help','version'])
        except getopt.error, why:
            #print('getopt error: %s\n%s' % (why, usage))
            sys.exit(-1)
        try:
            for opt in opts:
                if opt[0] == '-h' or opt[0] == '--help':
                    print usage
                    sys.exit(0)
                if opt[0] == '-p' or opt[0] == '--port':
                    self.port= int(opt[1])
        except ValueError, why:
            print 'Bad parameter \'%s\' for option %s: %s\n%s' % (
                                       opt[1], opt[0], why, usage)
        self.args = map(float, args)
        param = self.args
        return param

    def get_servers_input(self):
        '''Server's input is stored in a ServerState object'''
        if not self.so: return
        sockdata= str()
        while True:
            try:
                # Receive server data
                sockdata,addr= self.so.recvfrom(1024)
            except socket.error, emsg:
                #print("Waiting for data..............")
                pass
            if '***identified***' in sockdata:
                #print("Client connected..............")
                continue
            elif '***shutdown***' in sockdata:
                #print("Server has stopped the race. You were in %d place." % self.S.d['racePos'])
                self.shutdown()
                return
            elif '***restart***' in sockdata:
                # What do I do here?
                #print("Server has restarted the race.")
                # I haven't actually caught the server doing this.
                self.shutdown()
                return
            elif not sockdata: # Empty?
                continue       # Try again.
            else:
                self.S.parse_server_str(sockdata)
                #if self.debug: #print(self.S)
                break # Can now return from this function.

    def respond_to_server(self):
        if not self.so: return
        #if self.debug: #print(self.R)
        try:
            self.so.sendto(repr(self.R), (self.host, self.port))
        except socket.error, emsg:
            #print("Error sending to server: %s Message %s" % (emsg[1],str(emsg[0])))
            sys.exit(-1)

    def shutdown(self):
        if not self.so: return
        #print("Race terminated or %d steps elapsed. Shutting down." % self.maxSteps)
        self.so.close()
        self.so= None
        #sys.exit() # No need for this really.

class ServerState():
    'What the server is reporting right now.'
    def __init__(self):
        self.servstr= str()
        self.d= dict()

    def parse_server_str(self, server_string):
        'parse the server string'
        self.servstr= server_string.strip()[:-1]
        sslisted= self.servstr.strip().lstrip('(').rstrip(')').split(')(')
        for i in sslisted:
            w= i.split(' ')
            self.d[w[0]]= destringify(w[1:])

    def __repr__(self):
        out= str()
        for k in sorted(self.d):
            strout= str(self.d[k])
            if type(self.d[k]) is list:
                strlist= [str(i) for i in self.d[k]]
                strout= ', '.join(strlist)
            out+= "%s: %s\n" % (k,strout)
        return out

class DriverAction():
    '''What the driver is intending to do (i.e. send to the server).
    Composes something like this for the server:
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus 0)(meta 0) or
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus -90 -45 0 45 90)(meta 0)'''
    def __init__(self):
       self.actionstr= str()
       # "d" is for data dictionary.
       self.d= { 'accel':0.2,
                   'brake':0,
                  'clutch':0,
                    'gear':1,
                   'steer':0,
                   'focus':[-90,-45,0,45,90],
                    'meta':0
                    }

    def __repr__(self):
        out= str()
        for k in self.d:
            out+= '('+k+' '
            v= self.d[k]
            if not type(v) == list:
                out+= '%.3f' % v
            else:
                out+= ' '.join([str(x) for x in v])
            out+= ')'
        return out
        return out+'\n'

# == Misc Utility Functions
def destringify(s):
    '''makes a string into a value or a list of strings into a list of
    values (if possible)'''
    if not s: return s
    if type(s) is str:
        try:
            return float(s)
        except ValueError:
            #print("Could not find a value in %s" % s)
            return s
    elif type(s) is list:
        if len(s) < 2:
            return destringify(s[0])
        else:
            return [destringify(i) for i in s]

def clip(v,lo,hi):
    if v<lo: return lo
    elif v>hi: return hi
    else: return v

def drive_example(c):
    S= c.S.d
    R= c.R.d
    target_speed=c.param[0] #100

    l4 = float(S['track'][6])
    l3 = float(S['track'][7])
    l2 = float(S['track'][8])
    l1 = float(S['track'][8])
    mid= float(S['track'][9])
    r1 = float(S['track'][10])
    r2 = float(S['track'][11])
    r3 = float(S['track'][12])
    l4 = float(S['track'][13])


    if mid > 0:
        if l1<mid and r1<mid:
            X=9
            R['steer'] =0
        if l1>mid:
            if l3<l2+c.param[2]:
                R['steer'] = (((2*c.param[13])*PI)/180)#-0.1
                X=7
            else:
                R['steer'] = (((3*c.param[13])*PI)/180)#-0.1
        if r1>mid:
            if r3<r2+c.param[2]:
                R['steer'] = (((-2*c.param[13])*PI)/180)#+0.1
                X=7
            else:
                R['steer'] = (((-3*c.param[13])*PI)/180)#+0.1
    elif mid <0:
        R['steer']-= S['trackPos']*c.param[3] #.10
        R['steer']= clip(R['steer'],-1,1)
        if  S['speedX'] < 15:
            R['steer'] = S['angle']*c.param[2] / PI #10#


    # Damage Control
    target_speed-= S['damage'] * c.param[1] #.05
    if target_speed < 80: target_speed= 80

    # Throttle Control
    if S['speedX'] < target_speed - (R['steer']*c.param[6]): #50
        R['accel']+= c.param[4] #.01
    else:
        R['accel']-= c.param[5] #.01
    if S['speedX']<10:
       R['accel']+= 1/(S['speedX']+.1)

    # Traction Control System
    if ((S['wheelSpinVel'][2]+S['wheelSpinVel'][3]) -
       (S['wheelSpinVel'][0]+S['wheelSpinVel'][1]) > c.param[7]): #5
       R['accel']-= c.param[8] #.2
    R['accel']= clip(R['accel'],0,1)
    #c.param[12]=distance brom braking, 70 seemed OK
    if mid < c.param[12] and mid > 0 and  S['speedX'] > c.param[11]:
        R['brake'] = c.param[10] # brake value between 0 and 1
    else:
        R['brake'] =    0


    if (S['gear'] not in [0, 1, 2, 3, 4, 5, 6]):
     #   print "it is not in range"
        R['gear']=1
    ##up
    if (S['rpm']>c.param[9] and S['gear']==1):
        R['gear']=2
      #  print 'set gear to '+str(R['gear'])
    if S['rpm']>c.param[9] and S['gear']==2:
        R['gear']=3
      #  print 'set gear to '+str(R['gear'])
    if S['rpm']>c.param[9] and S['gear']==3:
        R['gear']=4
      #  print 'set gear to '+str(R['gear'])
    if S['rpm']>c.param[9] and S['gear']==4:
        R['gear']=5
      #  print 'set gear to '+str(R['gear'])
    if S['rpm']>c.param[9] and S['gear']==5:
        R['gear']=6
      #  print 'set gear to '+str(R['gear'])
    ##down
    if S['speedX']<20 and S['gear']==2:
        R['gear']=1
      #  print 'set gear to '+str(R['gear'])
    if S['speedX']<30 and S['gear']==3:
        R['gear']=2
      #  print 'set gear to '+str(R['gear'])
    if S['speedX']<50 and S['gear']==4:
        R['gear']=3
      #  print 'set gear to '+str(R['gear'])
    if S['speedX']<70 and S['gear']==5:
        R['gear']=4
      #  print 'set gear to '+str(R['gear'])
    if S['speedX']<100 and S['gear']==6:
        R['gear']=5
      #  print 'set gear to '+str(R['gear'])

    return

# ================ MAIN ================
if __name__ == "__main__":
    C= Client()
    for step in xrange(C.maxSteps,0,-1):
        C.get_servers_input()
        drive_example(C)
        C.respond_to_server()
    C.shutdown()