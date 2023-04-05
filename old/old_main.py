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
    """ Create the docker container

    Returns:
        docker_client.containers: container
    """
    print("Creating Docker container ...")
    container = docker_client.containers.create(
        image=docker_image, name=container_name, tty=True)
    container.start()
    return container


def execute_payload(payload_path):
    """ Execute the payload.sh script in the container

    Args:
        payload_path (String): the path of the payload.sh script
    """
    print("Executing payload.sh in the container ...")
    cmd = ["bash", "-c", payload_path + " -d " + str(duration)]
    exec_id = docker_client.api.exec_create(container=container_name, cmd=cmd)
    response = docker_client.api.exec_start(exec_id, stream=True)
    for line in response:
        print(line.decode('utf-8').strip())


def copy_file():
    """ Copy the pcap file from the container to the local disk
    """
    print("Copying file from the container to local disk ...")
    stream, _ = docker_client.api.get_archive(
        container_name, pcap_container_file)
    tar = tarfile.open(fileobj=io.BytesIO(next(stream)))
    tar.extractall(path=pcap_local_folder)
    tar.close()


def cleanup(container):
    """ Cleanup the container (stop and remove it)

    Args:
        container (docker_client.containers): the docker container to cleanup
    """
    print("Stopping the container ...")
    container.stop()

    # Remove container
    print("Removing the container ...")
    container.remove()

def pull_docker_image():
    """ Pull the docker image if not already exists
    """
    print("Pulling the docker image ...")
    try:
        docker_client.images.get(docker_image)
    except docker.errors.ImageNotFound:
        docker_client.images.pull(docker_image)

def verify_if_container_exists():
    """ Verify if the container already exists
    If it does exist, stop and remove it
    """
    try:
        container = docker_client.containers.get(container_name)
        print("Container is already running. Removing it ...")
        if container.status == "running":
            cleanup(container)
    except docker.errors.NotFound:
        pass


def get_ip():
    """ Get the IP of the container

    Returns:
        ip address (String): the IP of the container
    """
    container = docker_client.containers.get(container_name)
    return container.attrs['NetworkSettings']['IPAddress']


def attack_thread(attack_type, ip, duration):
    """ Create a thread for the attack

    Args:
        attack_type (String): the type of the attack
        ip (String): the IP of the container
        duration (int): the duration of the attack

    Returns:
        thread (threading.Thread): the thread
    """
    if attack_type == "syn":
        thread = threading.Thread(target=scapy_attacks.syn_flooding_attack, args=(
            ip, duration))
        return thread
    elif attack_type == "ping":
        thread = threading.Thread(target=scapy_attacks.ping_of_death, args=(
            ip, duration))
        return thread
    else:
        print("Unknown attack type: " + attack_type)


def read_pcap(pcap_file_path, summary=True):
    """ Read the pcap file

    Args:
        pcap_file_path (String): the path of the pcap file
        summary (bool, optional): If we want to log only the packets summary or full information.
        Defaults to True.
    """
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

    pull_docker_image()

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
