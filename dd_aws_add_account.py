import os

import boto3
from botocore.exceptions import ClientError

import requests

# originally written by Benjamin Burns @ Datadog

"""
http://boto3.readthedocs.io/en/latest/guide/configuration.html
Boto by default will look for configuration files in the following order:
1. Passing credentials as parameters in the boto.client() method
2. Passing credentials as parameters when creating a Session object
3. Environment variables
4. Shared credential file (~/.aws/credentials)
5. AWS config file (~/.aws/config)
6. Assume Role provider
7. Boto2 config file (/etc/boto.cfg and ~/.boto)
8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.
To use environment variables set the following before running the script:
export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY>
export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=<YOUR_DEFAULT_REGION>
"""

# To use customn aws config files uncomment the lines below.
# AWS_CONFIG_FILE='/path/to/config'
# AWS_SHARED_CREDENTIALS_FILE='/path/to/credentials'

DEVELOPMENT = True  # Set to false to use config files instead of enviromental vars
DATADOG_API_KEY = os.getenv('DATADOG_API_KEY', '<YOUR_DD_API_KEY>')
DATADOG_APP_KEY = os.getenv('DATADOG_APP_KEY', '<YOUR_DD_APP_KEY')
DD_URL = "https://app.datadoghq.com/api/v1/integration/aws?api_key=%s&application_key=%s" % (DATADOG_API_KEY, DATADOG_APP_KEY)

DD_AWS_INT_POLICY = """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "autoscaling:Describe*",
                "budgets:ViewBudget",
                "cloudtrail:DescribeTrails",
                "cloudtrail:GetTrailStatus",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "codedeploy:List*",
                "codedeploy:BatchGet*",
                "directconnect:Describe*",
                "dynamodb:List*",
                "dynamodb:Describe*",
                "ec2:Describe*",
                "ec2:Get*",
                "ecs:Describe*",
                "ecs:List*",
                "elasticache:Describe*",
                "elasticache:List*",
                "elasticfilesystem:DescribeFileSystems",
                "elasticfilesystem:DescribeTags",
                "elasticloadbalancing:Describe*",
                "elasticmapreduce:List*",
                "elasticmapreduce:Describe*",
                "es:ListTags",
                "es:ListDomainNames",
                "es:DescribeElasticsearchDomains",
                "kinesis:List*",
                "kinesis:Describe*",
                "lambda:List*",
                "logs:Get*",
                "logs:Describe*",
                "logs:FilterLogEvents",
                "logs:TestMetricFilter",
                "rds:Describe*",
                "rds:List*",
                "route53:List*",
                "s3:GetBucketTagging",
                "s3:ListAllMyBuckets",
                "ses:Get*",
                "sns:List*",
                "sns:Publish",
                "sqs:ListQueues",
                "support:*",
                "tag:getResources",
                "tag:getTagKeys",
                "tag:getTagValues"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}"""


# Safeguard against accidentilly using local policy in development
def verify_env_var_set():
    access_key = os.getenv('AWS_ACCESS_KEY_ID', '')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    if access_key and secret_key:
        return True
    return False

def get_sts_account_id():
    sts_client = boto3.client("sts")
    return sts_client.get_caller_identity()['Account']

def check_policy_role_exist(client, policy_arn, role_name):
    try:
        if client.get_policy(PolicyArn=policy_arn) or client.get_role(RoleName=role_name):
            return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            pass
        else:
            print(e)
            return True
    return False

def create_aws_policy(client, policy_name, policy_doc):
    try:
        response = client.create_policy(
            PolicyName=policy_name,
            Path='/',
            PolicyDocument=policy_doc,
            Description='DatadogAWSIntegrationPolicy'
        )
        return response['Policy']['Arn']
    except ClientError as e:
        print(e)
        raise SystemExit

# Temporary for dev purposes
ACCOUNT_ID = get_sts_account_id()
POLICY_NAME = 'DDAWS9'
POLICY_ARN = 'arn:aws:iam::%s:policy/%s' % (ACCOUNT_ID, POLICY_NAME)
ROLE_NAME = 'DDAWSROLE9'

if __name__ == '__main__':
    if DEVELOPMENT and not verify_env_var_set():
        print("Safeguarding against using aws config in development")
        raise SystemExit

    client = boto3.client('iam')

    print("Checking existence of Policy or Role")
    if check_policy_role_exist(client, POLICY_ARN, ROLE_NAME):
        raise SystemExit

    print("Creating new Policy")
    policy_arn = create_aws_policy(client, POLICY_NAME, DD_AWS_INT_POLICY)
    print("Created policy %s" % policy_arn)

    # Enable Datadog integration and retrieve ExternalId
    print("Configuring Datadog <> AWS Integration")

    r = requests.post(DD_URL, json={
        "account_id": ACCOUNT_ID,
        "filter_tags": ["env:staging"],
        "host_tags": ["account:staging","account:customer1"],
        "role_name": ROLE_NAME
    })

    if r.status_code == 200:
        EXTERNAL_ID = r.json()['external_id']
    else:
        print("Could not enable Datadog AWS integration")
        raise SystemExit

    assume_role_policy_document = """{
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "AWS": "arn:aws:iam::%s:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
              "StringEquals": {
                "sts:ExternalId": "%s"
              }
            }
          }
        ]
    }""" % (ACCOUNT_ID, EXTERNAL_ID)

    print("Creating AWS Role")
    try:
        response = client.create_role(
            Path='/',
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=assume_role_policy_document,
            Description='DatadogAWSIntegrationRole'
        )
        print(response['Role']['Arn'])
    except ClientError as e:
        print(e)
        raise SystemExit

    try:
        response = client.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn=POLICY_ARN
        )
        print(response)
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(e)
