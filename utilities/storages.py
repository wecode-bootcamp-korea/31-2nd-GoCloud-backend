import boto3, uuid

from django.conf import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
)

class FileUploader:
    def __init__(self, client, bucket_name):
        self.client = client
        self.bucket_name = bucket_name

    def upload(self, file, folder):
        file_id = str(uuid.uuid4())

        self.client.upload_fileobj(
            file,
            self.bucket_name,
            folder + file_id,
            ExtraArgs = {
                'ContentType':file.content_type
            }
        )
        return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}'
    
    def delete(self, file_name, bucket_name):
        self.s3.delete_object(Bucket=bucket_name, Key=file_name)


