import os
import pytest
from src.pcap import PcapManager


@pytest.fixture
def pcap_manager():
    pcap_local_folder = "./capture"
    pcap_file_path = "capture.pcap"
    return PcapManager(pcap_local_folder, pcap_file_path)


def test_read_pcap_summary(pcap_manager):
    pcap_manager.read_pcap(summary=True)
    assert os.path.exists("packet.log")
    with open("packet.log", "r") as f:
        packet_logs = f.readlines()
        assert "Ether / IP / ICMP" in packet_logs[0]


def test_read_pcap_full(pcap_manager):
    pcap_manager.read_pcap(summary=False)
    assert os.path.exists("packet.log")
    with open("packet.log", "r") as f:
        packet_logs = f.readlines()
        assert "###[ Ethernet ]### " in packet_logs[0]
