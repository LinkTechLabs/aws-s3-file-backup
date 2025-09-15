import pytest
from unittest.mock import MagicMock, patch
import boto3
from moto import mock_s3, mock_sns

# Mock the Lambda context
class MockContext:
    def __init__(self):
        self.function_name = "test-function"
        self.memory_limit_in_mb = 128
        self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
        self.aws_request_id = "test-request-id"

# Test event for S3 PUT event
s3_put_event = {
    "Records": [
        {
            "s3": {
                "bucket": {"name": "test-source-bucket"},
                "object": {"key": "test-file.txt"}
            }
        }
    ]
}

@mock_s3
@mock_sns
def test_lambda_handler():
    # Setup mock S3 and SNS
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    
    # Create source and destination buckets
    s3.create_bucket(Bucket="test-source-bucket")
    s3.create_bucket(Bucket="test-destination-bucket")
    
    # Create SNS topic
    topic_arn = sns.create_topic(Name="test-topic")["TopicArn"]
    
    # Set environment variables
    with patch.dict('os.environ', {
        'BACKUP_BUCKET': 'test-destination-bucket',
        'SNS_TOPIC_ARN': topic_arn
    }):
        # Import the lambda handler after setting up mocks
        from lambda_code import lambda_handler
        
        # Call the lambda handler
        result = lambda_handler(s3_put_event, MockContext())
        
        # Verify the file was copied
        response = s3.list_objects_v2(Bucket="test-destination-bucket")
        assert 'Contents' in response
        assert response['Contents'][0]['Key'] == 'test-file.txt'
        
        # Verify the SNS notification was sent
        # (Additional assertions can be added here)
        assert result['statusCode'] == 200
