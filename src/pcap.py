from scapy.all import rdpcap
import csv
from datetime import datetime


class PcapManager:

    def __init__(self, pcap_local_folder, pcap_file_path):
        self.pcap_local_folder = pcap_local_folder + "/"
        self.pcap_file_path = pcap_file_path

    def read_pcap(self, summary=True):
        """ Read the pcap file

        Args:
            pcap_file_path (String): the path of the pcap file
            summary (bool, optional): If we want to log only the packets summary or full information.
            Defaults to True.
        """
        print("Reading pcap file ...")
        packets = rdpcap(self.pcap_local_folder + self.pcap_file_path)
        with open("packet.log", "w") as f:
            for packet in packets:
                if summary:
                    f.write(str(packet.summary()) + "\n")
                else:
                    f.write(str(packet.show(dump=True)) + "\n")

    def read_pcap_to_csv(self):
        print("Reading pcap file ...")
        packets = rdpcap(self.pcap_local_folder + self.pcap_file_path)
        
        # Open a CSV file for writing
        with open('capture.csv', 'w', newline='') as csvfile:
            # Create a CSV writer
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(["srcIp", "dstIp", "srcPort", "dstPort", "type", "headerChecksum", "protocol", "version", "IHL", "length", "identification", "fragmentOffset", "TTL", "timer"])

            # Loop through each packet and write its headers to the CSV file
            for packet in packets:
                # Extract the relevant fields from the packet
                if packet.haslayer('IP'):
                    src_ip = packet['IP'].src
                    dst_ip = packet['IP'].dst
                    header_checksum = packet['IP'].chksum
                    protocol = packet['IP'].proto
                    version = packet['IP'].version
                    IHL = packet['IP'].ihl
                    identification = packet['IP'].id
                    fragment_offset = packet['IP'].frag
                    TTL = packet['IP'].ttl
                else:
                    src_ip = 'Undefined'
                    dst_ip = 'Undefined'
                    header_checksum = 'Undefined'
                    protocol = 'Undefined'
                    version = 'Undefined'
                    IHL = 'Undefined'
                    identification = 'Undefined'
                    fragment_offset = 'Undefined'
                    TTL = 'Undefined'

                if packet.haslayer('TCP'):
                    src_port = packet['TCP'].sport
                    dst_port = packet['TCP'].dport
                else:
                    src_port = 'Undefined'
                    dst_port = 'Undefined'

                length = len(packet)
                packet_type = packet['Ether'].type
                
                timer = packet.time

                # Convert the timer variable to a float
                timer_float = float(timer)

                # Create a datetime object from the float
                dt_object = datetime.fromtimestamp(timer_float)

                # Format the datetime object as a string
                dt_string = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")

                # Write the extracted fields to the CSV file
                writer.writerow([src_ip, dst_ip, src_port, dst_port, packet_type, header_checksum, protocol, version, IHL, length, identification, fragment_offset, TTL, dt_string])


    def __str__(self) -> str:
        return f"PcapManager(Find you pcap file here: {self.pcap_local_folder + self.pcap_file_path})"
