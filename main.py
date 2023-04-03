import docker
import time
import tarfile
import io

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


if __name__ == "__main__":
    print("Getting the Docker client ...")
    docker_client = docker.from_env()

    verify_if_container_exists()

    container = create_container()
    execute_payload("./payload.sh")

    # Sleep 20 seconds
    time.sleep(duration)

    copy_file()

    cleanup(container)
