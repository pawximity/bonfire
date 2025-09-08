from bonfire.error import DockerError
import docker


def process_args(args):
    """Processes the given CLI arguments.

    Dispatches to the appropriate resource removal functions 
    based on the flags provided. Uses smolder for dry runs.
    """
    client = docker.from_env()
    smolder = args.smolder
    if args.all:
        remove_all(client, dry_run=smolder)
        return
    if args.all_images:
        remove_images(client, all=True, dry_run=smolder)
    if args.images and not args.all_images:
        remove_images(client, dry_run=smolder)
    if args.containers:
        remove_containers(client, dry_run=smolder)
    if args.networks:
        remove_networks(client, dry_run=smolder)
    if args.volumes:
        remove_volumes(client, dry_run=smolder)


def remove_all(client, dry_run=False):
    """Removes all Docker resources.

    Burns images, containers, networks, and volumes from the
    local Docker environment. Skips defaults and respects
    smoldering if enabled.
    """
    remove_images(client, all=True, dry_run=dry_run)
    remove_containers(client, dry_run=dry_run)
    remove_networks(client, dry_run=dry_run)
    remove_volumes(client, dry_run=dry_run)


def remove_images(client, all=False, dry_run=False):
    """Removes Docker images.

    Burns dangling images by default, or all images if the
    `all` flag is set. Respects smoldering if enabled.
    """
    resource_type = "image"
    images = client.images.list() if all else client.images.list(
        filters={"dangling": True})
    for image in images:
        image_short_id = image.short_id
        print(burn_message(resource_type, image_short_id, dry_run=dry_run))
        if not dry_run:
            try:
                client.images.remove(image.id, force=True)
            except docker.errors.APIError:
                raise DockerError(resource_type, image_short_id)


def remove_containers(client, dry_run=False):
    """Removes Docker containers.

    Stops and burns all running containers from the local
    environment. Respects the smoldering.
    """
    resource_type = "container"
    for container in client.containers.list():
        container_short_id = container.short_id
        print(burn_message(resource_type, container_short_id, dry_run=dry_run))
        if not dry_run:
            try:
                container.stop()
                container.remove(force=True)
            except docker.errors.APIError:
                raise DockerError(resource_type, container_short_id)


def remove_networks(client, dry_run=False):
    """Removes Docker networks.

    Burns all user-created networks, skipping the default
    'bridge', 'host', and 'none'. Can be smoldered!
    """
    resource_type = "network"
    for network in client.networks.list():
        if network.name in ["bridge", "host", "none"]:
            continue
        network_short_id = network.short_id
        print(burn_message(resource_type, network_short_id, dry_run=dry_run))
        if not dry_run:
            try:
                network.remove()
            except docker.errors.APIError:
                raise DockerError(resource_type, network_short_id)


def remove_volumes(client, dry_run=False):
    """Removes Docker volumes.

    Burns all volumes from the local Docker environment.
    Respects smoldering if enabled.
    """
    resource_type = "volume"
    for volume in client.volumes.list():
        volume_id = volume.id
        print(burn_message(resource_type, volume_id, dry_run=dry_run))
        if not dry_run:
            try:
                volume.remove(force=True)
            except docker.errors.APIError:
                raise DockerError(resource_type, volume_id)


def burn_message(resource_type, resource_id, dry_run=False):
    prefix = "[*] Smoldering" if dry_run else "[-] Burning"
    return f"{prefix} {resource_type} {resource_id}"