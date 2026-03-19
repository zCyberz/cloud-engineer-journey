class AWSResource:
    def __init__(self,name,region,status):
        self.name=name
        self.region = region
        self.status = status

    def show(self):
        print(f"{self.name} - {self.region} - {self.status}")
    
    def stop(self):
        self.status ="stopped"
        print(f"{self.name} has been stopped!")
    
    def start(self):
        self.status="running"
        print(f"{self.name} is now running")

class EC2Instance(AWSResource):
    def __init__(self, name, region, status,instance_type):
        super().__init__(name, region, status)
        self.instance_type = instance_type
    def show(self):
        print(f"[EC2][{self.status.upper()}] {self.name} | {self.instance_type} | {self.region}")

class S3Bucket(AWSResource):
    def __init__(self, name, region, status,size_gb):
        super().__init__(name, region, status)
        self.size_gb = size_gb
    def show(self):
        print(f"[S3][{self.status.upper()}] {self.name} | {self.size_gb}GB | {self.region}")
    def upload(self,file_name):
        print(f"Uploaded {file_name} to {self.name}")

class RDSDatabase(AWSResource):
    def __init__(self, name, region, status,db_engine,storage_gb):
        super().__init__(name, region, status)
        self.db_engine = db_engine
        self.storage_gb = storage_gb
    def show(self):
        print(f"[RDS][{self.status.upper()}] {self.name} | {self.db_engine} | {self.storage_gb}GB | {self.region}")

    def backup(self):
        print(f"Backing up {self.name} to S3...")

rds = RDSDatabase("my-database", "ap-southeast-1", "running", "MySQL", 20)
rds.show()
rds.backup()
rds.stop()
rds.show()

"""ec2 = EC2Instance("web-server", "ap-southeast-1", "running", "t2.micro")
s3  = S3Bucket("my-bucket", "ap-southeast-1", "running", 50)

resources = [
    EC2Instance("web-server-01", "ap-southeast-1", "running", "t2.micro"),
    EC2Instance("db-server-01", "ap-southeast-1", "stopped", "t2.medium"),
    S3Bucket("my-bucket-01", "ap-southeast-1", "running", 50),
    S3Bucket("backup-bucket", "ap-southeast-1", "running", 100),
]

print("\n===== ALL RESOURCES =====")
for r in resources:
    r.show()

print("\n===== RUNNING ONLY =====")
for r in resources:
    if r.status == "running":
        r.show()

print("\n===== START ALL STOPPED =====")
for r in resources:
    if r.status == "stopped":
        r.start()

print("\n===== FINAL STATUS =====")
for r in resources:
    r.show()"""