# Import DockerManager from src/docker_management.py
from src.docker_management import DockerManager
from src.attacks import ScapyAttack
from src.pcap import PcapManager
import threading
import time

if __name__ == "__main__":
    docker_client = DockerManager("contackgen-ubuntu2204", 10)
    container = docker_client.create_container()
    container_ip = docker_client.get_container_ip()

    attack_client = ScapyAttack("127.0.0.1", container_ip, 2)

    tread_docker = threading.Thread(target=docker_client.execute_payload, args=(
        "./payload.sh",))
    thread_attack = threading.Thread(target=attack_client.ping_of_death)

    tread_docker.start()
    thread_attack.start()

    tread_docker.join()
    thread_attack.join()

    time.sleep(10)

    docker_client.copy_file_to_local()
    docker_client.cleanup(container)

    pcap_manager = PcapManager("./capture", "capture.pcap")
    pcap_manager.read_pcap(summary=False)
