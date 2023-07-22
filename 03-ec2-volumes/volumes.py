import boto3
import botocore

def get_unattached_volumes(ec2_client):
    unattached_volumes = []
    volumes_response = ec2_client.describe_volumes()
    for volume in volumes_response['Volumes']:
        if not volume['Attachments']:
            unattached_volumes.append(volume)
    return unattached_volumes

def delete_unattached_volumes(ec2_client):
    volumes_response = ec2_client.describe_volumes()
    for volume in volumes_response['Volumes']:
        if not volume['Attachments']:
            try:
                print(f"Deleting unattached volume...  {volume['VolumeId']}")
                ec2_client.delete_volume(VolumeId=volume['VolumeId'])
            except botocore.exceptions.ClientError as error:
                raise error

def get_attached_volumes(ec2_client):
    attached_volumes = []
    volumes_response = ec2_client.describe_volumes()
    for volume in volumes_response['Volumes']:
        if volume['Attachments']:
            attached_volumes.append(volume)
    return attached_volumes

def main():
    # Getting current AWS account id from assumed in profile
    boto3.client('sts').get_caller_identity().get('Account')

    ec2_client = boto3.client('ec2')

    attached_volumes = get_attached_volumes(ec2_client)
    # Print the details of attached volumes
    if attached_volumes:
        print("Attached Volumes:")
        for volume in attached_volumes:
            print(f"Volume ID: {volume['VolumeId']} " + f"Volume Type: {volume['VolumeType']}")
    else:
        print("No attached volumes found in account.")

    unattached_volumes = get_unattached_volumes(ec2_client)
    # Print the details of unattached volumes
    if unattached_volumes:
        print("Unattached Volumes:")
        for volume in unattached_volumes:
            print(f"Volume ID: {volume['VolumeId']} " + f"Volume Type: {volume['VolumeType']}")
            while True:
                user_input = input("Do you want to delete unattached volumes" + " (yes/no): ").strip().lower()
                if user_input == 'yes' or user_input == 'y':
                    delete_unattached_volumes(ec2_client)
                    return True
                elif user_input == 'no' or user_input == 'n':
                    print("Cancelling...")
                    return False
                else:
                    print("Invalid input. Please enter 'yes' or 'no' cancelling...")
                    break
    else:
        print("No unattached volumes found in account.")

if __name__ == "__main__":
    main()
