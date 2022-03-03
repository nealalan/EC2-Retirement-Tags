import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [{
            'Name': 'event.code',
            'Values': ['instance-retirement','instance-stop']
         }
     ]

    # capture the instances containing filter values
    instances = ec2.describe_instance_status(Filters=filters)

    # grab the instance status objects, contining the event code, event description, Id
    instance = instances['InstanceStatuses']

    # AWS doesn't role off the actions for approximately a week - they only update the event description
    # adding logic to ignore the instances that are listed as "Completed"
    instancelist = []    
    for instanceid in instance:
        if 'Completed' in str(instanceid['Events'][0]):
            print("Action already completed: ", instanceid['InstanceId'])
        else:
            print("Adding: ", instanceid['InstanceId'])
            instancelist.append(instanceid['InstanceId'])

    # print the instances for logging purposes
    print(instancelist)

    # make sure there are actually instances to tag.
    if len(instancelist) > 0:
        # Adding The Tags
        TagInstance = ec2.create_tags(
            Resources =
                instancelist,
            Tags = [
               {
                   'Key':'RetirementScheduled',
                   'Value':'Yes'
                }
            ]
        )
        print("Adding Tags")
    else:
        print("Nothing to update")
