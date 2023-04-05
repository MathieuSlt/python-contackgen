import pytest
from src.docker_management import DockerManager


@pytest.fixture(scope="session")
def docker_manager():
    return DockerManager(container_name="test_container", duration=10)


def test_create_container(docker_manager):
    """Test the creation of a container

    Args:
        docker_manager (DockerManager): Our Docker class
    """
    container = docker_manager.create_container()
    assert container.status == "created"
    docker_manager.cleanup(container)


def test_get_container_ip(docker_manager):
    """Test the get_container_ip function

    Args:
        docker_manager (DockerManager): Our Docker class
    """
    docker_manager.pull_docker_image()
    container = docker_manager.create_container()
    assert docker_manager.get_container_ip() is not None
    docker_manager.cleanup(container)
