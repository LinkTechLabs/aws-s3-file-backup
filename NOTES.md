# File Backup - Notes

## Topics
- AWS S3
- AWS Backup
- IAM Policies
- Cross-region Replication
- Lifecycle Policies

## Resources
- [AWS Backup Documentation](https://docs.aws.amazon.com/aws-backup/)
- [S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/best-practices.html)

### AWS Commands
- copy to s3 
    - `aws s3 cp /path/to/local/file s3://bucket-name`


## Habit Check-in
### 2025-09-15 11:12:17 - 2hr
**What I did**: 
- Created 2 s3 buckets (Source & Backup)
- Created an SNS topic to receive notifications
- Lambda function to trigger backup & notify via SNS
- End to end testing

**Blockers**: 
- IAM permissions
    - lambda function needed more permissions to trigger backup & interact with s3

**Next Step**: 
- Add enhancements
    - cloudtrail s3 data event auditing
    - Security hardening
    - Monitoring & alerts
    - Reliability and Scale
    - Cost optimization
    - Frontend uploader

## Notes
- [Add your notes here]
