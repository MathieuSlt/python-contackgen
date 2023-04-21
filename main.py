#!/usr/bin/env python
from src.docker_management import DockerManager
from src.attacks import ScapyAttack
from src.pcap import PcapManager
import threading
import time
import argparse

if __name__ == "__main__":

    # create an ArgumentParser object
    parser = argparse.ArgumentParser(description='ContackGen')

    # add the arguments
    parser.add_argument('-d', '--duration', type=int, required=True, help='Duration of the attack in seconds (higher than 5)')
    parser.add_argument('-a', '--attack', type=int, choices=[1, 2, 3], required=True, help='Type of attack : 1 (Ping of Death), 2 (Syn Flooding), 3 (Smurf attack)')

    # parse the arguments
    args = parser.parse_args()

    # access the values of the arguments
    duration = args.duration
    attack = args.attack

    # example usage messages for errors
    if duration < 5:
        print('Error: duration must be a positive integer higher than 5')
        parser.print_usage()
        exit()

    if attack not in [1, 2, 3]:
        print('Error: attack must be one of the following values: 1 (Ping of Death), 2 (Syn Flooding), 3 (Smurf attack)')
        parser.print_usage()
        exit()


    docker_client = DockerManager("contackgen-ubuntu2204", duration)
    print(docker_client)
    container = docker_client.create_container()
    container_ip = docker_client.get_container_ip()

    attack_client = ScapyAttack("127.0.0.1", container_ip, duration)
    print(attack_client)

    tread_docker = threading.Thread(target=docker_client.execute_payload, args=(
        "./payload.sh",))
    thread_attack = None

    match attack:
        case 1:
            thread_attack = threading.Thread(target=attack_client.ping_of_death)
        case 2:
            thread_attack = threading.Thread(target=attack_client.syn_flooding_attack)
        case 3:
            thread_attack = threading.Thread(target=attack_client.smurf_attack)

    tread_docker.start()
    thread_attack.start()

    tread_docker.join()
    thread_attack.join()

    docker_client.copy_file_to_local()
    docker_client.cleanup(container)

    pcap_manager = PcapManager(
        docker_client.get_pcap_local_folder(), "capture.pcap")
    print(pcap_manager)

    # pcap_manager.read_pcap(summary=False)
    pcap_manager.read_pcap_to_csv()
