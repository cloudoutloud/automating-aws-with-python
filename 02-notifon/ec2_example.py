# coding: utf-8
# This will create the following EC2 instances, keypair & inbound sg rules

import boto3
import os, stat 

session = boto3.Session(profile_name='cr-labs-CF')
ec2 = session.resource('ec2')
key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
key.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
ami_name = 'amzn2-ami-hvm-2.0.20190508-x86_64-gp2'
filters = [{'Name': 'name', 'Values': [ami_name]}]
img = ec2.Image(id='ami-0009a33f033d8b7b6')
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
inst = instances[0]
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(IpPermissions=[{'FromPort': 22, 'ToPort': 22, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '90.211.148.217/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort': 80, 'ToPort': 80, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
print("All resources created")

