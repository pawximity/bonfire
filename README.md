## Bonfire

**Bonfire** is a controlled fire for resetting your local Docker environment.  
It removes Docker resources (images, containers, networks, and volumes) from a local dev machine.  
You can burn everything or you can **smolder**, which performs a non-destructive dry run.  

---

## Features

- Burn dangling images, all images, or both
- Burn all containers
- Burn user-created networks (skips defaults: `bridge`, `host`, `none`)
- Burn all volumes
- Smoldering for safe, non-destructive dry runs
- Simple

---

## Requirements

- Python 3.8+
- [Docker SDK for Python](https://pypi.org/project/docker/) (`pip install docker`)
- Local Docker daemon running

---

## Usage

```bash
# Install locally
pip install -e .

# Start the bonfire
bonfire ignite --all

# Smolder (dry run)
bonfire ignite --all --smolder