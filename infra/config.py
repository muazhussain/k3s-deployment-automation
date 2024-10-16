class Config:
    """
    Represents the configuration for the cluster.
    """
    def __init__(self, project_name, instance_type, ami, region, availability_zone) -> None:
        self.project_name = project_name
        self.instance_type = instance_type
        self.ami = ami
        self.region = region
        self.availability_zone = availability_zone