import boto3
from moto import mock_aws
@mock_aws
def test_s3():
    s3 = boto3.client("s3",region_name="ap-southeast-1")

    s3.create_bucket(
        Bucket= "my-test-bucket",
        CreateBucketConfiguration= {"LocationConstraint":"ap-southeast-1"}
    )
    
    s3.put_object(
        Bucket="my-test-bucket",
        Key="reports/report.csv",
        Body="name,age\nAn,20\nBinh,21"
    )

    s3.put_object(
        Bucket="my-test-bucket",
        Key="logs/server.log",
        Body="Server started at 09:00"
    )

    s3.delete_object(
        Bucket="my-test-bucket",
        Key="logs/server.log"
    )
    print("\nDeleted logs/server.log!")

    response=s3.list_objects(Bucket="my-test-bucket")
    print("\nFiles in bucket:")
    for obj in response["Contents"]:
        print(f" -{obj['Key']}({obj['Size']} bytes)")
    
    response2 = s3.list_objects(Bucket="my-test-bucket")
    print("\nFiles after delete:")
    for obj in response2["Contents"]:
        print(f"  - {obj['Key']} ({obj['Size']} bytes)")



test_s3()