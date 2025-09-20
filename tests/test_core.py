from bonfire import core
import pytest
from types import SimpleNamespace


def test_remove_images_dry_run(monkeypatch):
    image_id = "image_id"
    metrics = {"image": 0}
    removed_ids = []

    mock_image = SimpleNamespace(id=image_id, short_id="short_id")
    client = SimpleNamespace()
    client.images = SimpleNamespace(list=None, remove=None)

    monkeypatch.setattr(client.images,
                        "list",
                        lambda filters=None: [mock_image])
    monkeypatch.setattr(
        client.images,
        "remove",
        lambda image_id, force=False: removed_ids.append(image_id))

    core.remove_images(client, metrics, all=False, dry_run=True)
    assert metrics["image"] == 1
    assert removed_ids == []


def test_remove_images(monkeypatch):
    image_id = "image_id"
    metrics = {"image": 0}
    removed_ids = []

    mock_image = SimpleNamespace(id=image_id, short_id="short_id")
    client = SimpleNamespace()
    client.images = SimpleNamespace(list=None, remove=None)

    monkeypatch.setattr(client.images,
                        "list",
                        lambda filters=None: [mock_image])
    monkeypatch.setattr(
        client.images,
        "remove",
        lambda image_id, force=False: removed_ids.append(image_id))

    core.remove_images(client, metrics, all=False, dry_run=False)
    assert metrics["image"] == 1
    assert removed_ids == [image_id]


def test_remove_images_docker_error(monkeypatch):
    from bonfire.error import DockerError
    from docker.errors import APIError

    image_id = "image_id"
    metrics = {"image": 0}
    removed_ids = []

    mock_image = SimpleNamespace(id=image_id, short_id="short_id")
    client = SimpleNamespace()
    client.images = SimpleNamespace(list=None, remove=None)

    monkeypatch.setattr(client.images,
                        "list",
                        lambda filters=None: [mock_image])

    def mock_remove(image_id, force=True):
        raise APIError("remove images test")

    monkeypatch.setattr(client.images, "remove", mock_remove)

    with pytest.raises(DockerError) as e:
        core.remove_images(client, metrics, all=False, dry_run=False)

    assert metrics["image"] == 0
    assert removed_ids == []


def test_remove_all_images(monkeypatch):
    image_id1, image_id2 = "image_id1", "image_id2"
    short_id1, short_id2 = "short_id1", "short_id2"
    metrics = {"image": 0}
    removed_ids = []

    mock_image1 = SimpleNamespace(id=image_id1, short_id=short_id1)
    mock_image2 = SimpleNamespace(id=image_id2, short_id=short_id2)
    client = SimpleNamespace()
    client.images = SimpleNamespace(list=None, remove=None)

    monkeypatch.setattr(client.images,
                        "list",
                        lambda filters=None: [mock_image1, mock_image2])
    monkeypatch.setattr(
        client.images,
        "remove",
        lambda image_id1, force=False: removed_ids.append(image_id1))
    monkeypatch.setattr(
        client.images,
        "remove",
        lambda image_id2, force=False: removed_ids.append(image_id2))

    core.remove_images(client, metrics, all=True, dry_run=False)
    assert metrics["image"] == 2
    assert removed_ids == [image_id1, image_id2]


def test_remove_containers_dry_run(monkeypatch):
    container_id = "container_id"
    metrics = {"container": 0}

    mock_container = SimpleNamespace(
        id=container_id,
        short_id="short_id",
        stopped=False,
        removed=False,
        stop=lambda: setattr(mock_container, "stopped", True),
        remove=lambda: setattr(mock_container, "removed", True))

    client = SimpleNamespace()
    client.containers = SimpleNamespace(list=None)

    monkeypatch.setattr(client.containers,
                        "list",
                        lambda filters=None: [mock_container])

    core.remove_containers(client, metrics, dry_run=True)
    assert metrics["container"] == 1
    assert mock_container.stopped == False
    assert mock_container.removed == False


def test_remove_containers(monkeypatch):
    container_id = "container_id"
    metrics = {"container": 0}

    mock_container = SimpleNamespace(
        id=container_id,
        short_id="short_id",
        stopped=False,
        removed=False,
        stop=lambda: setattr(mock_container, "stopped", True),
        remove=lambda force: setattr(mock_container, "removed", True))

    client = SimpleNamespace()
    client.containers = SimpleNamespace(list=None)

    monkeypatch.setattr(client.containers,
                        "list",
                        lambda filters=None: [mock_container])

    core.remove_containers(client, metrics, dry_run=False)
    assert metrics["container"] == 1
    assert mock_container.stopped == True
    assert mock_container.removed == True


def test_remove_containers_docker_error(monkeypatch):
    from bonfire.error import DockerError
    from docker.errors import APIError

    container_id = "container_id"
    metrics = {"container": 0}

    def mock_remove(force=True):
        raise APIError("remove container test")

    mock_container = SimpleNamespace(
        id=container_id,
        short_id="short_id",
        stopped=False,
        removed=False,
        stop=lambda: setattr(mock_container, "stopped", True),
        remove=mock_remove)

    client = SimpleNamespace()
    client.containers = SimpleNamespace(list=None)

    monkeypatch.setattr(client.containers,
                        "list",
                        lambda filters=None: [mock_container])

    with pytest.raises(DockerError) as e:
        core.remove_containers(client, metrics, dry_run=False)

    assert metrics["container"] == 0
    assert mock_container.stopped == True
    assert mock_container.removed == False