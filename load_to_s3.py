import os
import glob
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_file(directory: str) -> str:
    """Get the latest json file in the specified directory."""
    list_of_files = glob.glob(os.path.join(directory, "*.json"))
    if not list_of_files:
        logging.warning(f"No files found in {directory} matching pattern {'*.json'}.")
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    logging.info(f"Latest file found: {latest_file}")
    return latest_file

def upload_to_s3(file_path: str, bucket_name: str, s3_key: str) -> bool:
    """Upload a file to an S3 bucket."""
    logging.info(f"Initializing S3 client for bucket: {bucket_name}")

    s3_client = boto3.client('s3', region_name='us-east-2')

    try:
        logging.info(f"Uploading {file_path} to S3 bucket {bucket_name} with key {s3_key}...")
        s3_client.upload_file(file_path, bucket_name, s3_key)
        logging.info("Upload successful.")
        return True
    except ClientError as e:
        logging.error(f"Error uploading file to S3: {e}")
        return False

def main():
    logging.info("Starting the load to S3 process...")

    bucket_name = os.getenv("S3_BUCKET_NAME")
    if not bucket_name:
        logging.error("S3_BUCKET_NAME not found in .env file")
        return

    data_dir = "data"
    latest_file = get_latest_file(data_dir)

    if not latest_file:
        logging.warning("No JSON file found. Exiting.")
        return

    file_name = os.path.basename(latest_file)
    s3_key = f"raw/weather/{file_name}"
    upload_to_s3(latest_file, bucket_name, s3_key)

    logging.info("Load to S3 process completed.")

if __name__ == "__main__":
    main()