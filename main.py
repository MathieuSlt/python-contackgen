import docker
import time
import tarfile
import io
import scapy_attacks
import threading
from scapy.all import rdpcap

container_name = "contackgen-ubuntu2204"
pcap_container_file = "/data/capture.pcap"
pcap_local_folder = "./capture"
docker_image = "fersuy/contackgen-ubuntu2204:1.1.0"
duration = 10


def create_container():
    print("Creating Docker container ...")
    container = docker_client.containers.create(
        image=docker_image, name=container_name, tty=True)
    container.start()
    return container


def execute_payload(payload_path):
    print("Executing payload.sh in the container ...")
    cmd = ["bash", "-c", payload_path + " -d " + str(duration)]
    exec_id = docker_client.api.exec_create(container=container_name, cmd=cmd)
    response = docker_client.api.exec_start(exec_id, stream=True)
    for line in response:
        print(line.decode('utf-8').strip())


def copy_file():
    print("Copying file from the container to local disk ...")
    stream, _ = docker_client.api.get_archive(
        container_name, pcap_container_file)
    tar = tarfile.open(fileobj=io.BytesIO(next(stream)))
    tar.extractall(path=pcap_local_folder)
    tar.close()


def cleanup(container):
    print("Stopping the container ...")
    container.stop()

    # Remove container
    print("Removing the container ...")
    container.remove()


def verify_if_container_exists():
    try:
        container = docker_client.containers.get(container_name)
        print("Container is already running. Removing it ...")
        if container.status == "running":
            cleanup(container)
    except docker.errors.NotFound:
        pass


def get_ip():
    container = docker_client.containers.get(container_name)
    return container.attrs['NetworkSettings']['IPAddress']


def attack_thread(attack_type, ip, duration):
    if attack_type == "syn":
        thread = threading.Thread(target=scapy_attacks.Syn_Flooding_Attack, args=(
            ip, duration))
        return thread
    elif attack_type == "ping":
        thread = threading.Thread(target=scapy_attacks.Ping_of_death, args=(
            ip, duration))
        return thread
    else:
        print("Unknown attack type: " + attack_type)


def read_pcap(pcap_file_path, summary=True):
    print("Reading pcap file ...")
    packets = rdpcap(pcap_local_folder + pcap_file_path)
    with open("packet.log", "w") as f:
        for packet in packets:
            if summary:
                f.write(str(packet.summary()) + "\n")
            else:
                f.write(str(packet.show(dump=True)) + "\n")


if __name__ == "__main__":
    print("Getting the Docker client ...")
    docker_client = docker.from_env()

    verify_if_container_exists()

    container = create_container()

    ip = get_ip()
    print("IP: " + ip)

    # Threads creation
    tread_container = threading.Thread(target=execute_payload, args=(
        "./payload.sh",))
    thread_attack = attack_thread("ping", ip, 2)

    # Threads start
    tread_container.start()
    time.sleep(4)
    thread_attack.start()

    # Threads join
    tread_container.join()
    thread_attack.join()

    # Sleep duration seconds
    time.sleep(int(duration))

    copy_file()

    cleanup(container)

    read_pcap("/capture.pcap", summary=False)
