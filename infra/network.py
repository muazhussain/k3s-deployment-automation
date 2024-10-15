import pulumi_aws.ec2 as ec2

class Network:
    """
    Represents a network in AWS. This includes a VPC, a public subnet,
    a private subnet, an internet gateway, and a NAT gateway.
    """
    def __init__(self, config) -> None:
        self.config = config
        self.vpc = self._create_vpc()
        self.public_subnet = self._create_public_subnet()
        self.private_subnet = self._create_private_subnet()
        self.internet_gateway = self._create_internet_gateway()
        self.nat_gateway = self._create_nat_gateway()
        self._setup_route_tables()
    
    def _create_vpc(self, vpc_name = 'vpc', cidr_block = '10.0.0.0/16', enable_dns_support = True, enable_dns_hostnames = True):
        return ec2.Vpc(
            f'{self.config.project_name}-{vpc_name}',
            cidr_block = cidr_block,
            enable_dns_support = enable_dns_support,
            enable_dns_hostnames = enable_dns_hostnames,
            tags = {
                'Name': f'{self.config.project_name}-{vpc_name}'
            }
        )
    
    def _create_public_subnet(self, subnet_name = 'public-subnet', cidr_block = '10.0.1.0/24', map_public_ip_on_launch = True):
        return ec2.Subnet(
            f'{self.config.project_name}-{subnet_name}',
            vpc_id = self.vpc.id,
            cidr_block = cidr_block,
            availability_zone = self.config.availability_zone,
            map_public_ip_on_launch = map_public_ip_on_launch,
            tags = {
                'Name': f'{self.config.project_name}-{subnet_name}'
            }
        )
    
    def _create_private_subnet(self, subnet_name = 'private-subnet', cidr_block = '10.0.2.0/24'):
        return ec2.Subnet(
            f'{self.config.project_name}-{subnet_name}',
            vpc_id = self.vpc.id,
            cidr_block = cidr_block,
            availability_zone = self.config.availability_zone,
            tags = {
                'Name': f'{self.config.project_name}-{subnet_name}'
            }
        )
    
    def _create_internet_gateway(self, internet_gateway_name = 'internet-gateway'):
        return ec2.InternetGateway(
            f'{self.config.project_name}-{internet_gateway_name}',
            vpc_id = self.vpc.id,
            tags = {
                'Name': f'{self.config.project_name}-{internet_gateway_name}'
            }
        )
    
    def _create_nat_gateway(self, nat_gateway_name = 'nat-gateway'):
        return ec2.NatGateway(
            f'{self.config.project_name}-{nat_gateway_name}',
            subnet_id = self.public_subnet.id,
            tags = {
                'Name': f'{self.config.project_name}-{nat_gateway_name}'
            }
        )

    def _setup_route_tables(self, public_route_table_name = 'public-route-table', private_route_table_name = 'private-route-table'):
        public_route_table = ec2.RouteTable(
            f'{self.config.project_name}-{public_route_table_name}',
            vpc_id = self.vpc.id,
            routes = [
                {'cidr_block': '0.0.0.0/0', 'gateway_id': self.internet_gateway.id}
            ],
            tags = {
                'Name': f'{self.config.project_name}-{public_route_table_name}'
            }
        )

        ec2.RouteTableAssociation(
            f'{self.config.project_name}-public-route-table-association',
            subnet_id = self.public_subnet.id,
            route_table_id = public_route_table.id
        )

        private_route_table = ec2.RouteTable(
            f'{self.config.project_name}-{private_route_table_name}',
            vpc_id = self.vpc.id,
            routes = [
                {'cidr_block': '0.0.0.0/0', 'nat_gateway_id': self.nat_gateway.id}
            ],
            tags = {
                'Name': f'{self.config.project_name}-{private_route_table_name}'
            }
        )

        ec2.RouteTableAssociation(
            f'{self.config.project_name}-private-route-table-association',
            subnet_id = self.private_subnet.id,
            route_table_id = private_route_table.id
        )
