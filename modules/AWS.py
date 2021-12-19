import boto3
from botocore.exceptions import ClientError

global session
session = boto3.Session()

class S3Object(object):
    def __init__(self):
        self.resource = session.resource('s3')
        self.client = self.resource.meta.client
    
    def createBucket(self, bucketName: str):
        self.client.create_bucket(Bucket=bucketName)
    
    def enableVersioning(self, bucketName: str):
        self.resource.BucketVersioning(bucketName).enable()

    def checkBucket(self, bucketName: str) -> bool:
        try:
            self.client.head_bucket(Bucket=bucketName)
        except ClientError:
            return False
        
        return True
    
    def uploadFile(self, filePath: str, bucket: str, key: str):
        return self.client.upload_file(filePath, bucket, key)

    def getObject(self, bucket: str, key: str):
        return self.client.get_object(
            Bucket = bucket,
            Key = key
        )
    
    def getVersion(self, bucket: str, key: str):
        return self.getObject(bucket, key)['VersionId']


class CloudFormationObject(object):
    def __init__(self):
        self.client = session.client('cloudformation')
    
    def stackExists(self, stackId: str):
        try:
            self.client.describe_stacks(StackName = stackId)
        except ClientError:
            return False
        
        return True

    def createOrUpdateStack(self, stackId: str, templateUrl: str, parameters: any):
        if self.stackExists(stackId):
            self.updateStack(stackId, templateUrl, parameters)
        else:
            self.createStack(stackId, templateUrl, parameters)
    
    def createStack(self, stackId: str, templateUrl: str, parameters: any):
        self.client.create_stack(
            StackName = stackId,
            TemplateURL = templateUrl, 
            Parameters = parameters,
            Capabilities= ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND']
        )
    
    def updateStack(self, stackId: str, templateUrl: str, parameters: any):
        self.client.update_stack(
            StackName = stackId,
            TemplateURL = templateUrl, 
            Parameters = parameters,
            Capabilities= ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND']
        )


S3 = S3Object()
CloudFormation = CloudFormationObject()
