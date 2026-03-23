import boto3
from moto import mock_aws

@mock_aws
def test_security_group():
    ec2 = boto3.client("ec2", region_name="ap-southeast-1")

    # Tạo VPC trước
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]
    print(f"✅ Created VPC: {vpc_id}")

    # Tạo Security Group
    sg = ec2.create_security_group(
        GroupName="web-server-sg",
        Description="Security group for web server",
        VpcId=vpc_id
    )
    sg_id = sg["GroupId"]
    print(f"✅ Created Security Group: {sg_id}")

    # Thêm inbound rules
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 443,
                "ToPort": 443,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": "1.2.3.4/32"}]
            }
        ]
    )
    print("✅ Added inbound rules!")

    # Xem rules
    response = ec2.describe_security_groups(GroupIds=[sg_id])
    sg_info = response["SecurityGroups"][0]
    print(f"\n📋 Security Group: {sg_info['GroupName']}")
    print("Inbound rules:")
    for rule in sg_info["IpPermissions"]:
        print(f"  Port {rule['FromPort']} → {rule['IpRanges'][0]['CidrIp']}")

test_security_group()