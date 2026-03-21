import boto3
from moto import mock_aws

class S3Manager:
    def __init__(self,bucket_name,region):
        self.bucket_name=bucket_name
        self.region = region
        self.s3 = boto3.client("s3",region_name=region)

    def create_bucket(self):
        self.s3.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={"LocationConstraint":self.region}
        )
        print(f"Created Bucket:{self.bucket_name}")
    
    def upload_file(self,key,content):
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key= key,
            Body=content
        )
        print(f"Upload: {key}")

    def list_files(self):
        response=self.s3.list_objects(Bucket=self.bucket_name)
        print("\nFiles in bucket:")
        for obj in response["Contents"]:
            print(f" -{obj['Key']}({obj['Size']} bytes)")
    
    def delete_file(self,key):
        self.s3.delete_object(
            Bucket=self.bucket_name,
            Key = key
        )
        print(f"Deleted:{key}")

    def generate_url(self,key,expiry=3600):
        url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name , "Key": key},
            ExpiresIn=expiry
        )
        print(f"URL:{url[:60]}")
@mock_aws
def main():
    s3_manager = S3Manager("my-company-bucket", "ap-southeast-1")
    s3_manager.create_bucket()
    s3_manager.upload_file("reports/jan.csv", "date,revenue\n2026-01,5000")
    s3_manager.upload_file("reports/feb.csv", "date,revenue\n2026-02,6000")
    s3_manager.upload_file("logs/server.log", "Server started!")
    s3_manager.list_files()
    s3_manager.delete_file("logs/server.log")
    s3_manager.list_files()
    s3_manager.generate_url("reports/jan.csv")

main()