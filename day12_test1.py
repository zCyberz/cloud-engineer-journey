import boto3
from moto import mock_aws
import os

@mock_aws
def test_s3_advanced():
    s3 = boto3.client("s3", region_name="ap-southeast-1")

    # Tạo bucket
    s3.create_bucket(
        Bucket="my-bucket",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-1"}
    )

    # 1. Tạo file local để test
    with open("test_file.txt", "w") as f:
        f.write("Hello from local file!")

    # 2. Upload file từ ổ đĩa
    s3.upload_file("test_file.txt", "my-bucket", "uploads/test_file.txt")
    print("✅ Uploaded file from disk!")

    # 3. Download file từ S3
    s3.download_file("my-bucket", "uploads/test_file.txt", "downloaded_file.txt")
    print("✅ Downloaded file!")

    # 4. Đọc file vừa download
    with open("downloaded_file.txt", "r") as f:
        content = f.read()
    print(f"📄 Content: {content}")

    # 5. Copy file sang bucket khác
    s3.create_bucket(
        Bucket="backup-bucket",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-1"}
    )
    s3.copy_object(
        CopySource={"Bucket": "my-bucket", "Key": "uploads/test_file.txt"},
        Bucket="backup-bucket",
        Key="backup/test_file.txt"
    )
    print("✅ Copied to backup bucket!")

    # 6. Cleanup local files
    os.remove("test_file.txt")
    os.remove("downloaded_file.txt")
    print("🗑️ Cleaned up local files!")

    s3.put_bucket_versioning(
        Bucket="my-bucket",
        VersioningConfiguration={"Status":"Enabled"}
    )
    print(f"Versioning enabled")

    for i in range(1,4):
        s3.put_object(
            Bucket="my-bucket",
            Key="versioned_file.txt",
            Body=f"Version {i}"
        )
        print(f"Upload version {i}")

    response = s3.list_object_versions(Bucket="my-bucket")
    print("\nAll Versions: ")
    for version in response["Versions"]:
        print(f"  - {version['Key']}  | VersionId: {version['VersionId'][:8]}...")

test_s3_advanced()