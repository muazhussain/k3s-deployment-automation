import pulumi_aws.ec2 as ec2

class Instances:
    def __init__(self, config, network, security):
        """
        Initialize the instances.

        :param config: The configuration for the instances
        :param network: The network to create the instances in
        :param security: The security group to assign to the instances
        :return: None
        """
        self.config = config
        self.network = network
        self.security = security
        self.master = self._create_master_instance()
        self.workers = self._create_worker_instances()
        self.git_runner = self._create_git_runner_instance()

    def _create_master_instance(self):
        return ec2.Instance(
            f'{self.config.project_name}-master',
            instance_type = self.config.instance_type,
            ami = self.config.ami,
            subnet_id = self.network.private_subnet.id,
            vpc_security_group_ids = [self.security.security_group.id],
            key_name = self.security.key_pair.key_name,
            tags = {
                'Name': f'{self.config.project_name}-master',
            }
        )

    def _create_worker_instances(self, worker_count = 2):
        return [
            ec2.Instance(f'{self.config.project_name}-worker-{i + 1}',
                instance_type = self.config.instance_type,
                ami = self.config.ami,
                subnet_id = self.network.private_subnet.id,
                vpc_security_group_ids = [self.security.security_group.id],
                key_name = self.security.key_pair.key_name,
                tags = {
                    'Name': f'{self.config.project_name}-worker-{i + 1}',
                }
            ) for i in range(worker_count)
        ]

    def _create_git_runner_instance(self):
        return ec2.Instance(f'{self.config.project_name}-git-runner',
            instance_type = self.config.instance_type,
            ami = self.config.ami,
            subnet_id = self.network.public_subnet.id,
            vpc_security_group_ids = [self.security.security_group.id],
            key_name = self.security.key_pair.key_name,
            tags = {
                'Name': f'{self.config.project_name}-git-runner',
            }
        )