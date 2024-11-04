# S3 Bucket Copy Tool

## Description

A Python script that copies all objects from one Amazon S3 bucket to another, allowing for separate configurations for each bucket, including different AWS credentials, regions, and endpoint URLs. This tool is useful for migrating data between S3 buckets, backing up data, or syncing buckets across different AWS accounts or regions.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shamspias/s3-bucket-copy-tool.git
   cd s3-bucket-copy-tool
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   - Create a `.env` file in the project root directory.
   - Add your source and destination bucket configurations as per the `example.env` provided.

4. **Run the Script**

   ```bash
   python script.py
   ```

## Why You Need This

- **Data Migration**: Easily migrate data between S3 buckets in different AWS accounts or regions.
- **Backup Solution**: Create backups of your S3 data in another bucket.
- **Synchronization**: Sync data between S3-compatible services with different endpoints.
- **Flexibility**: Customize configurations for each bucket, including credentials and endpoints.
