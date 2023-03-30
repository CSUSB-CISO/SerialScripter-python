import boto3
import datetime

#def lambda_handler(event, context):
def BackupFunction(event, context):
# Create a new EC2 client
    ec2 = boto3.client('ec2')

    # Get a list of all running instances
    reservations = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    ).get('Reservations', [])

    # Loop through each running instance
    for reservation in reservations:
        for instance in reservation['Instances']:
            # Get the instance ID, name, and region
            instance_id = instance['InstanceId']
            instance_name = [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0]
            instance_region = instance['Placement']['AvailabilityZone'][:-1]

            # Create a backup AMI of the instance
            create_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            ami_name = f"{instance_name}-backup-{create_time}"
            response = ec2.create_image(
                InstanceId=instance_id,
                Name=ami_name,
                Description=f"Backup of instance {instance_id}",
                NoReboot=True
            )

            # Print the AMI ID for debugging purposes
            print(f"Created AMI {response['ImageId']} for instance {instance_id}")
