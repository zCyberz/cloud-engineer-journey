import boto3
from moto import mock_aws

class S3Manager:
    def __init__(self,region):
        self.region=region
        self.s3 = boto3.client("s3",region_name=region)

    def create_bucket(self,name):
        self.s3.create_bucket(
            Bucket=name,
            CreateBucketConfiguration={"LocationConstraint":self.region}
        )
        print(f"Created Bucket:{name}")

    def list_buckets(self):
        response = self.s3.list_buckets()
        print(f"All buckets: ")
        for bucket in response['Buckets']:
            print(f" - {bucket['Name']}")

    def upload_file(self,bucket,key,context):
        self.s3.put_object(
            Bucket=bucket,
            Key = key,
            Body = context
        )
        print(f"Bucket: {bucket} - Key: {key} - Body: {context}")

    def list_files(self,bucket):
        response = self.s3.list_objects(Bucket=bucket)
        print(f"\nFiles in {bucket}")
        for obj in response['Contents']:
            print(f"  - {obj['Key']} ({obj['Size']} bytes)")

    def delete_file(self,bucket,key):
        self.s3.delete_object(
            Bucket=bucket,
            Key=key
        )
        print(f"\nDeleted {bucket} - {key} !")

@mock_aws
def main():
    manager = S3Manager("ap-southeast-1")
    manager.create_bucket("my-bucket-01")
    manager.create_bucket("my-bucket-02")
    manager.list_buckets()
    manager.upload_file("my-bucket-01", "data/file.txt", "Hello AWS!")
    manager.upload_file("my-bucket-01", "logs/app.log", "App started!")
    manager.list_files("my-bucket-01")
    manager.delete_file("my-bucket-01", "logs/app.log")
    manager.list_files("my-bucket-01")

main()