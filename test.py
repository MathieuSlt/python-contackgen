# Import DockerManager from src/docker_management.py
from src.docker_management import DockerManager


docker_client = DockerManager("contackgen-ubuntu2204", 10)
docker_client.run("./payload.sh")
