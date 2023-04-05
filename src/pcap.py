from scapy.all import rdpcap


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
