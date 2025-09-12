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