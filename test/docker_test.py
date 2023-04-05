from src.docker_management import DockerManager

if __name__ == "__main__":
    docker_client = DockerManager("contackgen-ubuntu2204", 10)
    docker_client.run("./payload.sh")
