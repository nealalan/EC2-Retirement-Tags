import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [{
            'Name': 'tag:RetirementScheduled',
            'Values': ['Yes']
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all tagged instances
    TaggedInstances = [instance.id for instance in instances]

    #print the tagged instances for logging purposes
    print(TaggedInstances)

    #make sure there are actually instances to remove tags on.
    if len(TaggedInstances) > 0:
        #perform the startup

        TagInstance = ec2_client.delete_tags(
            Resources =
                TaggedInstances,
            Tags = [
                {
                    'Key':'RetirementScheduled',
                    'Value':'Yes'
                }
            ]
        )
        print("Removing Tags")
    else:
        print("Nothing to update")
