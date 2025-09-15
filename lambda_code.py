import os
import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    """
    AWS Lambda function to copy objects from source to backup bucket
    and send notification via SNS.
    
    Environment Variables:
    - BACKUP_BUCKET: Name of the backup S3 bucket
    - SNS_TOPIC_ARN: ARN of the SNS topic for notifications
    """
    try:
        # Get environment variables
        backup_bucket = os.environ['BACKUP_BUCKET']
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
        
        # Process each record in the event
        for record in event.get('Records', []):
            if 's3' not in record:
                continue
                
            # Get bucket and key from the S3 event
            source_bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            # Log the copy operation
            logger.info(f'Copying {key} from {source_bucket} to {backup_bucket}')
            
            # Copy the object to the backup bucket
            copy_source = {'Bucket': source_bucket, 'Key': key}
            s3.copy_object(
                Bucket=backup_bucket,
                Key=key,
                CopySource=copy_source
            )
            
            # Send notification
            message = f"Successfully backed up {key} to {backup_bucket}"
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject="S3 Backup Notification",
                Message=message
            )
            
            logger.info(f'Successfully processed {key}')
            
        return {
            'statusCode': 200,
            'body': 'Backup completed successfully'
        }
        
    except KeyError as e:
        error_msg = f'Missing environment variable: {str(e)}'
        logger.error(error_msg)
        raise Exception(error_msg)
        
    except ClientError as e:
        error_msg = f'Error accessing AWS service: {str(e)}'
        logger.error(error_msg)
        raise Exception(error_msg)
        
    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        logger.error(error_msg)
        raise Exception(error_msg)
