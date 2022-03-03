# EC2-Retirement-Tags

## Application

This application will check the instance statues action / event codes for an instance that is slated for hardware retirement and must be stopped and started to be moved to new hardware. This will check to ensure any instances stopped by AWS will be started back up with automation.

## Testing / Console review

You can not see the action / event codes for an instance unless you use the CLI. The following command will show you any that exist:

```bash
$ aws ec2 describe-instance-status --instance-ids <INSTANCE_IDS> | grep "InstanceId\|Code\|Description"
```

## IAM Roles & Policies

1. Tag-Retirement-Instances_Role contains Policy with access to EC2 & CloudWatch Logs.
2. Start-Stopped-Retirement-Instances_Role contains Policy with access EC2, KMS & CloudWatch Logs.
3. Remove-Retirement-Instances-Tag_Role contains Policy with access to EC2 & CloudWatch logs.

## Lambda Functions

1. Tag-Retirement-Instances function - Tag instances with ‘event.code - instance-retirement' in their status. 
2. Start-Stopped-Retirement-Instances function - Start any stopped instances that have the tag RetirementScheduled = Yes 
3. Remove-Retirement-Instances-Tag function - Remove the RetirementScheduled tag after the instance has been started. We do not want these tags to exist after the instances are started incase a user intentionally stopped the instance.

## EventBridge Triggeres

1. Run Tag-Retirement-Instances Lambda using cron(00 23 * * ? *)
2. Run Start-Stopped-Retirement-Instances Lambda every 5 minutes using rate(5 minutes)
3. Run Remove-Retirement-Instances-Tag once a day just before the Tag-Retirement-Instances Lambda using cron(50 22 * * ? *)

## Implement with CloudFormation

1. Update TagRetirementInstances-Policy.template REGION and ACCOUNT_ID place holders in the template (alternatively this could be converted to use Parameters.) 
2. Create a new CloudFormation Stack and populate the Parameter Policy Name: Tag-Retirement-Instances_Policy
3. Launch the Stack.
4. Grab the TagRetirementInstances-Role.template
5. Create a new CloudFormation Stack and populate the Parameters Role Name: Tag-Retirement-Instances_Role; ARN with the Policy ARN; Services: lambda.amazonaws.com
6. Launch the Stack.
7. Repeat 1-6 for the StartStoppedRetirementInstances-Policy.template and StartStoppedRetirementInstances-Role.template
8. Repeat 1-6 for the RemoveRetirementInstancesTag-Policy.template and RemoveRetirementInstancesTag-Role.template
9. Verify all stacks have launched successfully.
10. Zip each of the Lambda functions into zip files called Tag-Retirement-Instances.zip, Remove-Retirement-Instances-Tag.zip and Start-Stopped-Retirement-Instances.zip
11. Upload the zip files to a new S3 bucket
12. Grab the RetirementInstancesLambdaFunctions.template
13. Create a new CloudFormation Stack and populate the Parameters S3Bucket with the bucket the zip files are in and 3 Role fields with the 3 IAM Role ARNs.
14. Launch the stack.
