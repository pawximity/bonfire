class BonfireError(Exception):
    pass


class DockerError(BonfireError):

    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"Could not remove {resource_type} {resource_id}")