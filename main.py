import docker

imageId = "fersuy/contackgen-ubuntu2204:1.0.0"
containerName = "contackgen-ubuntu2204"

client = docker.from_env()

print("Pulling image...")
container = client.containers.run(imageId, detach=True, name=containerName)
print(container.logs())
print(container.id)


container.stop()
container.remove()
# print(container.status)