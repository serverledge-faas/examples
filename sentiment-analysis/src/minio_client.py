import os
from minio import Minio

class MinIoClient:
    
    def __init__(self, endpoint=None, 
                 access_key=None, 
                 secret_key=None, 
                 secure=None, 
                 default_bucket=None):
        """
        Initialize MinIO client with connection parameters.
        
        Args:
            endpoint: MinIO server endpoint (host:port)
            access_key: Access key for authentication
            secret_key: Secret key for authentication
            secure: Use HTTPS if True, HTTP if False
            default_bucket: Default bucket name for operations
        """
        self.endpoint = endpoint or os.getenv("MINIO_ENDPOINT", "160.80.97.154:9000")
        self.access_key = access_key or os.getenv("MINIO_ACCESS_KEY", "minio")
        self.secret_key = secret_key or os.getenv("MINIO_SECRET_KEY", "minio123")
        self.secure = secure if secure is not None else (os.getenv("MINIO_SECURE", "false").lower() == "true")
        self.default_bucket = default_bucket or os.getenv("MINIO_BUCKET", "serverledge")
        
        # Initialize the Minio client
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )


    def ensure_bucket(self, bucket_name=None):
        if bucket_name == None:
            bucket_name = self.default_bucket
        """Create bucket if it does not exist"""
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
        else:
            print(f"Bucket {bucket_name} already exists")

    def exists(self, object_name, bucket_name=None):
        if bucket_name == None:
            bucket_name = self.default_bucket
        try:
            self.client.stat_object(bucket_name, object_name)
            return True
        except:
            return False
        
    def upload_file(self, local_path, object_name, bucket_name=None, override=False):
        """Upload local file to MinIO"""
        if bucket_name == None:
            bucket_name = self.default_bucket
        self.ensure_bucket(bucket_name)
        obj_exists = self.exists(object_name, bucket_name)
        if not override and obj_exists:
            print(f"! Upload canceled. Object {bucket_name}/{object_name} already exists.")
        self.client.fput_object(bucket_name, object_name, local_path)
        # print(f"Uploaded {local_path} → {bucket_name}/{object_name}")

    def download_file(self, object_name, local_path, bucket_name=None):
        """Download file from MinIO"""
        if bucket_name == None:
            bucket_name = self.default_bucket
        try:
            self.client.fget_object(bucket_name, object_name, local_path)
            # print(f"Downloaded {bucket_name}/{object_name} → {local_path}")
        except Exception as e:
            print(f"Error while downloading file from MinIO: {str(e)}")
            return False
        return True