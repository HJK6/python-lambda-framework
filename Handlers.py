from modules.AWS import S3
from modules.Config import ASSETS_BUCKET, INFRASTRUCTURE_ZIP


# Sample Handler function. Returns the deployed version, and also returns the date modified if the verbose input prop is passed in as True
def getDeploymentDetailsHandler(event, context):
    version = S3.getVersion(ASSETS_BUCKET, INFRASTRUCTURE_ZIP)

    if 'verbose' in event and event['verbose'] == True:
        object = S3.getObject(ASSETS_BUCKET, INFRASTRUCTURE_ZIP)  
        lastModified = object['ResponseMetadata']['HTTPHeaders']['last-modified'];

        return {'Details': 'The currently deployed version ({}) was modified on {}'.format(version, lastModified)}
    else:
        return {'Details': 'The currently deployed version is: {}'.format(version)}
        
        
