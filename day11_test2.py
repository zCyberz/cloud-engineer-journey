import boto3
from moto import mock_aws

class EC2Manager:
    def __init__(self,region):
        self.region =region
        self.ec2=boto3.client("ec2",region_name=region)

    def create_instance(self,instance_type):
        response = self.ec2.run_instances(
            ImageId="ami-12345678",
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type
    ) 
        instance_id = response["Instances"][0]["InstanceId"]
        print(f"Created: {instance_id}")
        return instance_id

    def list_instances(self):
        response  = self.ec2.describe_instances()
        print("\n📋 Instances:")
        for r in response["Reservations"]:
            for i in r["Instances"]:
                print(f"  {i['InstanceId']} | {i['State']['Name']} | {i['InstanceType']}")

    def stop_instance(self,instance_ids):
        self.ec2.stop_instances(InstanceIds=[instance_ids])
        print(f"\n⏹️ Stopped: {instance_ids}")
        self.list_instances()

    def terminate_instance(self,instance_ids):
        self.ec2.terminate_instances(InstanceIds=[instance_ids])
        print(f"\n⏹️ Terminated: {instance_ids}")
        self.list_instances()


@mock_aws
def main():
    manager = EC2Manager("ap-southeast-1")
    
    # Tạo 2 instances
    id1 = manager.create_instance("t2.micro")
    id2 = manager.create_instance("t2.medium")
    
    # List tất cả
    manager.list_instances()
    
    # Stop instance 1
    manager.stop_instance(id1)
    manager.list_instances()
    
    # Terminate instance 2
    manager.terminate_instance(id2)
    manager.list_instances()

main()