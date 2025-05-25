import boto3
import os

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
ENDPOINT_URL = "https://storage.yandexcloud.net"
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Создание клиента
s3_client = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_directory(local_dir, bucket, s3_base_path=""):
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            # Относительный путь
            relative_path = os.path.relpath(local_path, local_dir)
            # Путь для S3
            s3_path = os.path.join(s3_base_path, relative_path).replace("\\", "/")

            # Загрузка
            s3_client.upload_file(local_path, bucket, s3_path)
            print(f"Загружен {local_path} на s3://{bucket}/{s3_path}")


upload_directory("images", BUCKET_NAME, "images")

upload_directory("annotations", BUCKET_NAME, "annotations")

# Проверка
response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="")
for obj in response.get("Contents", []):
    print(obj["Key"])



