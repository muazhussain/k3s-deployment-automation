import pulumi
from config import Config
from network import Network
from security import Security
from instance import Instance

def main():
    config = Config(
        project_name = 'k3s-deployment',
        instance_type = 't3.small',
        ami = 'ami-003c463c8207b4dfa',
        region = 'ap-southeast-1',
        availability_zone = 'ap-southeast-1a'
    )

    network = Network(config)
    security = Security(config, network.vpc.id)
    instance = Instance(config, network, security)

    # Output the instance public IP addresses
    pulumi.export('git_runner_public_ip', instance.git_runner.public_ip)
    pulumi.export('master_private_ip', instance.master.private_ip)
    pulumi.export('worker-1_private_ip', instance.workers[0].private_ip)
    pulumi.export('worker-2_private_ip', instance.workers[1].private_ip)

if __name__ == '__main__':
    main()