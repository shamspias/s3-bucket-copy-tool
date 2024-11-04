import os
import sys
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


def setup_logging():
    """Configure logging format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        stream=sys.stdout
    )


def load_config():
    """Load configuration from .env file and validate required keys."""
    load_dotenv()
    config = {
        'source': {
            'aws_access_key_id': os.getenv('SOURCE_AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('SOURCE_AWS_SECRET_ACCESS_KEY'),
            'aws_region': os.getenv('SOURCE_AWS_REGION'),
            'bucket_name': os.getenv('SOURCE_BUCKET'),
            'endpoint_url': os.getenv('SOURCE_ENDPOINT_URL')
        },
        'destination': {
            'aws_access_key_id': os.getenv('DESTINATION_AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('DESTINATION_AWS_SECRET_ACCESS_KEY'),
            'aws_region': os.getenv('DESTINATION_AWS_REGION'),
            'bucket_name': os.getenv('DESTINATION_BUCKET'),
            'endpoint_url': os.getenv('DESTINATION_ENDPOINT_URL'),
            'prefix': os.getenv('DESTINATION_PREFIX', '')
        }
    }

    required_keys = [
        ('source', 'aws_access_key_id'),
        ('source', 'aws_secret_access_key'),
        ('source', 'aws_region'),
        ('source', 'bucket_name'),
        ('destination', 'aws_access_key_id'),
        ('destination', 'aws_secret_access_key'),
        ('destination', 'aws_region'),
        ('destination', 'bucket_name')
    ]

    missing_keys = [
        f"{section.upper()}_{key.upper()}"
        for section, key in required_keys
        if not config[section].get(key)
    ]

    if missing_keys:
        logging.error(f"Missing required configuration keys: {', '.join(missing_keys)}")
        exit(1)

    return config


def get_s3_client(config_section):
    """Initialize and return an S3 client using the provided configuration section."""
    return boto3.client(
        's3',
        aws_access_key_id=config_section['aws_access_key_id'],
        aws_secret_access_key=config_section['aws_secret_access_key'],
        region_name=config_section['aws_region'],
        endpoint_url=config_section.get('endpoint_url')
    )


def copy_objects(source_s3_client, destination_s3_client, config):
    """Copy all objects from the source bucket to the destination bucket."""
    source_bucket = config['source']['bucket_name']
    destination_bucket = config['destination']['bucket_name']
    destination_prefix = config['destination']['prefix']

    paginator = source_s3_client.get_paginator('list_objects_v2')
    try:
        for page in paginator.paginate(Bucket=source_bucket):
            for obj in page.get('Contents', []):
                copy_source = {'Bucket': source_bucket, 'Key': obj['Key']}
                destination_key = os.path.join(destination_prefix, obj['Key'])
                logging.info(f"Copying {obj['Key']} to {destination_key}")
                # Fetch the object's ACL to maintain permissions (optional)
                # acl = source_s3_client.get_object_acl(Bucket=source_bucket, Key=obj['Key'])
                # Copy the object
                destination_s3_client.copy_object(
                    CopySource=copy_source,
                    Bucket=destination_bucket,
                    Key=destination_key,
                    verify=False
                )
                # Set the object's ACL to match the source (optional)
                # destination_s3_client.put_object_acl(
                #     Bucket=destination_bucket,
                #     Key=destination_key,
                #     AccessControlPolicy=acl
                # )
    except ClientError as e:
        logging.error(f"Error copying objects: {e}")
        exit(1)


def main():
    setup_logging()
    config = load_config()
    source_s3_client = get_s3_client(config['source'])
    destination_s3_client = get_s3_client(config['destination'])
    copy_objects(source_s3_client, destination_s3_client, config)
    print("_____Complete______")


if __name__ == '__main__':
    main()
