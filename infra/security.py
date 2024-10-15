import os
import pulumi_aws as aws

class Security:
    """
    Create the security group and key pair for the instances.
    """
    def __init__(self, config, vpc_id):
        self.config = config
        self.security_group = self._create_security_group(vpc_id)
        self.key_pair = self._create_key_pair()

    def _create_security_group(self, vpc_id):
        return aws.ec2.SecurityGroup(
            f'{self.config.project_name}-security-group',
            vpc_id = vpc_id,
            ingress = [
                {
                    'from_port': 22,
                    'to_port': 22,
                    'protocol': 'tcp',
                    'cidr_blocks': ['0.0.0.0/0']
                },
                {
                    'protocol': 'tcp',
                    'from_port': 6443,
                    'to_port': 6443,
                    'cidr_blocks': ['0.0.0.0/0'],
                },
            ],
            egress = [
                {
                    'from_port': 0,
                    'to_port': 0,
                    'protocol': '-1',
                    'cidr_blocks': ['0.0.0.0/0']
                }
            ],
            tags = {
                'Name': f'{self.config.project_name}-security-group'
            }
        )
    
    def _create_key_pair(self):
        public_key = os.getenv('PUBLIC_KEY')
        return aws.ec2.KeyPair(f'{self.config.project_name}-key-pair',
            key_name = f'{self.config.project_name}-key-pair',
            public_key = public_key
        )