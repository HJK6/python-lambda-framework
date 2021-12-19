import os
import zipfile
import subprocess
import shutil
from modules.AWS import S3, CloudFormation
import sys
from modules.Config import (
    ASSETS_BUCKET,
    INFRASTRUCTURE_ZIP, 
    INFRASTRUCTURE_TEMPLATE,
    INFRASTRUCTURE_REQUIREMENTS,
    INFRASTRUCTURE_TEMPLATE_URL,
    INFRASTRUCTURE_STACK_ID,
    PYTHON,
)
from typing import Sequence

def installRequirements():
    subprocess.run('{} -m pip install -r ./templates/{} --target=./dist/temp'.format(PYTHON, INFRASTRUCTURE_REQUIREMENTS), shell=True)

def deleteRequirements():
    shutil.rmtree('./dist/temp')

def getAllFilePaths(directory: str, exclusions: Sequence[str] = []):
    # initializing empty file paths list
    file_paths = []
  
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename in exclusions:
                continue
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    # returning all file paths
    return file_paths   

def checkPreReqs():
    # Creates necessary path if it does not already exist
    os.makedirs('./dist/temp', exist_ok=True)

    # Creates bucket if it does not already exist
    if not S3.checkBucket(ASSETS_BUCKET):
        sys.exit("The S3 Bucket {} does not exist, or you do not have access".format(ASSETS_BUCKET))
    
    # Confirms that Versioning is enabled (necessary for lambda updates)
    S3.enableVersioning(ASSETS_BUCKET)

    # Validates that the Handlers file exists
    if not os.path.exists('Handlers.py'):
        sys.exit("No Handlers.py file exists")

    # Validates that the CloudFormation template exists
    if not os.path.exists('./templates/{}'.format(INFRASTRUCTURE_TEMPLATE)):
        sys.exit("No {} file exists in the ./templates folder".format(INFRASTRUCTURE_TEMPLATE))

    # Validates that the requirements file exists
    if not os.path.exists('./templates/{}'.format(INFRASTRUCTURE_REQUIREMENTS)):
        sys.exit("No {} file exists in the ./templates folder".format(INFRASTRUCTURE_REQUIREMENTS))

def packageInfrastructure():
    checkPreReqs()

    outZip = zipfile.ZipFile('./dist/{}'.format(INFRASTRUCTURE_ZIP), 'w', zipfile.ZIP_DEFLATED)
    
    for file in getAllFilePaths('./modules', ['DevOps.py']):
        outZip.write(file)
    
    installRequirements()

    for file in getAllFilePaths('./dist/temp'):
        outZip.write(file, file.replace('./dist/temp', ''))

    outZip.write('./Handlers.py')

    outZip.close()


def deployInfrastructure():
    S3.uploadFile('./dist/{}'.format(INFRASTRUCTURE_ZIP), ASSETS_BUCKET, INFRASTRUCTURE_ZIP)
    S3.uploadFile('./templates/{}'.format(INFRASTRUCTURE_TEMPLATE), ASSETS_BUCKET, INFRASTRUCTURE_TEMPLATE)

    CloudFormation.createOrUpdateStack(
        stackId = INFRASTRUCTURE_STACK_ID, 
        templateUrl = INFRASTRUCTURE_TEMPLATE_URL, 
        parameters = [
            {
                "ParameterKey": "Version",
                "ParameterValue": S3.getVersion(
                    bucket = ASSETS_BUCKET, 
                    key = INFRASTRUCTURE_ZIP
                    )
            },
            {
                "ParameterKey": "AssetsBucket",
                "ParameterValue": ASSETS_BUCKET
            },
            {
                "ParameterKey": "InfrastructureZip",
                "ParameterValue": INFRASTRUCTURE_ZIP
            }
        ]
        )
    
    return

def deployHandlers():
    packageInfrastructure()
    deployInfrastructure()

