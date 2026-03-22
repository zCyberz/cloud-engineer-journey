import boto3
from moto import mock_aws

@mock_aws
def test_ec2():
    ec2 = boto3.client("ec2", region_name="ap-southeast-1")

    # Tạo 2 instances
    response = ec2.run_instances(
        ImageId="ami-12345678",
        MinCount=2,
        MaxCount=2,
        InstanceType="t2.micro"
    )

    # Lấy instance IDs
    instance_ids = [i["InstanceId"] for i in response["Instances"]]
    print(f"Created: {instance_ids}")

    # List instances
    def list_instances():
        res = ec2.describe_instances()
        print("\n📋 Instances:")
        for r in res["Reservations"]:
            for i in r["Instances"]:
                print(f"  {i['InstanceId']} | {i['State']['Name']} | {i['InstanceType']}")

    list_instances()

    # Stop instance đầu tiên
    ec2.stop_instances(InstanceIds=[instance_ids[0]])
    print(f"\n⏹️ Stopped: {instance_ids[0]}")
    list_instances()

    # Terminate instance thứ 2
    ec2.terminate_instances(InstanceIds=[instance_ids[1]])
    print(f"\n🗑️ Terminated: {instance_ids[1]}")
    list_instances()

test_ec2()
