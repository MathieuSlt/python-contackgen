import docker
import tarfile
import io


class DockerManager:
    """
    Class for managing docker containers.
    """

    def __init__(self, container_name, duration):
        self.pcap_container_file = "/data/capture.pcap"
        self.pcap_local_folder = "./capture"
        self.docker_image = "fersuy/contackgen-ubuntu2204:1.1.0"
        self.docker_client = docker.from_env()
        self.container_name = container_name
        self.duration = duration

    def pull_docker_image(self) -> None:
        """ Pull the docker image if not already exists
        """
        print("Pulling the docker image ...")
        try:
            self.docker_client.images.get(self.docker_image)
        except docker.errors.ImageNotFound:
            self.docker_client.images.pull(self.docker_image)

    # @staticmethod
    def verify_if_container_exists(self) -> None:
        """ Verify if the container already exists
        If it does exist, stop and remove it
        """
        try:
            container = self.docker_client.containers.get(self.container_name)
            print("Container is already running. Removing it ...")
            if container.status == "running":
                self.cleanup(container)
        except docker.errors.NotFound:
            pass

    def create_container(self) -> docker.models.containers.Container:
        """ Create the docker container

        Returns:
            docker_client.containers: container
        """
        self.verify_if_container_exists()

        print("Creating Docker container ...")
        container = self.docker_client.containers.create(
            image=self.docker_image, name=self.container_name, tty=True)
        container.start()
        return container

    def execute_payload(self, payload_path: str) -> None:
        """ Execute the payload.sh script in the container

        Args:
            payload_path (str): the path of the payload.sh script
        """
        print("Executing payload.sh in the container ...")
        cmd = ["bash", "-c", payload_path + " -d " + str(self.duration)]
        exec_id = self.docker_client.api.exec_create(
            container=self.container_name, cmd=cmd)
        response = self.docker_client.api.exec_start(exec_id, stream=True)
        for line in response:
            print(line.decode('utf-8').strip())

    def copy_file_to_local(self) -> None:
        """ Copy the pcap file from the container to the local disk
        """
        print("Copying file from the container to local disk ...")
        stream, _ = self.docker_client.api.get_archive(
            self.container_name, self.pcap_container_file)
        tar = tarfile.open(fileobj=io.BytesIO(next(stream)))
        tar.extractall(path=self.pcap_local_folder)
        tar.close()

    def cleanup(self, container: docker.models.containers.Container) -> None:
        """ Cleanup the container (stop and remove it)

        Args:
            container (docker_client.containers): the docker container to cleanup
        """
        print("Stopping the container ...")
        container.stop()

        # Remove container
        print("Removing the container ...")
        container.remove()

    def get_container_ip(self) -> str:
        """ Get the IP of the container

        Returns:
            ip address (str): the IP of the container
        """
        container = self.docker_client.containers.get(self.container_name)
        return container.attrs['NetworkSettings']['IPAddress']

    def run(self, payload_path: str) -> None:
        """ Run the docker container, execute the payload.sh script and copy the pcap file to the local disk

        Args:
            payload_path (str): the path of the payload.sh script
        """
        container = self.create_container()
        self.execute_payload(payload_path)
        self.copy_file_to_local()
        self.cleanup(container)
