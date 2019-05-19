# coding: utf-8

import boto3

session = boto3.Session(profile_name='cr-labs-CF')
ec2 = session.resource('ec2')
ids = ['i-0b344280640ca12bc']

ec2.instances.filter(InstanceIds=ids).stop()
print('Instance has been stopped')
ec2.instances.filter(InstanceIds=ids).terminate()
print('Instance has been terminated')