#!/usr/bin/python                                                                   
import os
import shutil
import readline
import fileinput
import time
import sys

#Capture all required information from user
n = None
while n is None:
        nodenumber = raw_input("Enter your node number from 10 to 30: ")
        try:
                n = int(nodenumber)
        except ValueError:
                print "Not a number."
homessid = raw_input("Enter your home SSID: ")
homewirelesskey = raw_input("Enter your home wireless key: ")
presharedkey = raw_input("Enter your IPSEC key: ")


#Set file source and destination
source = '.'
dest1 = '/etc/network'
dest2 = '/etc'
dest3 = '/etc/wpa_supplicant'

#Place files in correct location based on text inside of each file
files = os.listdir(source)
for f in files:
        if (f.startswith("interfaces")):
                shutil.copy(f, dest1)
        elif (f.startswith("ipsec") or f.startswith("rc.local") or f.startswith("iptables.conf")):
                shutil.copy(f, dest2)
        elif (f.startswith("wpa_supplicant")):
                shutil.copy(f, dest3)

#Edit network files
for line in fileinput.input("/etc/wpa_supplicant/wpa_supplicant.conf", inplace=True):
        print line.replace("homessid", homessid,),
for line in fileinput.input("/etc/wpa_supplicant/wpa_supplicant.conf", inplace=True):
        print line.replace("homewirelesskey", homewirelesskey,),
for line in fileinput.input("/etc/network/interfaces", inplace=True):
        print line.replace("XX", nodenumber,),
for line in fileinput.input("/etc/rc.local", inplace=True):
        print line.replace("XX", nodenumber,),
for line in fileinput.input("/etc/iptables.conf", inplace=True):
        print line.replace("XX", nodenumber,),

#Restart networking
print "[+]Restart Networking..."
os.system("systemctl daemon-reload")
os.system("systemctl restart networking")
time.sleep(5)   #Delay for 5 seconds. Ensure networking is restarted prior to installing openswan

#Update Node
print "[+]Updating Node..."
os.system("apt-get update -y && apt-get upgrade -y > /dev/null")
time.sleep(5)

#Install openswan
print "[+]Installing openswan..."
os.system("apt-get install openswan -y > /dev/null")
time.sleep(5)

#Install VIM
print "[+]Installing apps..."
os.system("apt-get install vim dos2unix -y > /dev/null")
time.sleep(5)

#Edit IPSEC files
for line in fileinput.input("/etc/ipsec.conf", inplace=True):
        print line.replace("XX", nodenumber,),
for line in fileinput.input("/etc/ipsec.secrets", inplace=True):
        print line.replace("presharedkey", presharedkey,),
for line in fileinput.input("/etc/ipsec.secrets", inplace=True):
        print line.replace("XX", nodenumber,),

#Restart IPSEC
print "[+]Restart IPSEC..."
os.system("systemctl restart ipsec")
os.system("systemctl enable ipsec")

