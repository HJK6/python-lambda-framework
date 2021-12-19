### Deployment Variables

# Name of your S3 Bucket where deployment assets will be stored
# Make sure that versioning is enabled, or lambdas will not update 
ASSETS_BUCKET = "test-lambda-handler"
INFRASTRUCTURE_ZIP = "Infrastructure.zip"
INFRASTRUCTURE_TEMPLATE = "cloudformation.yaml"
INFRASTRUCTURE_REQUIREMENTS = "requirements.txt"
INFRASTRUCTURE_TEMPLATE_URL = 'https://{}.s3.amazonaws.com/{}'.format(ASSETS_BUCKET, INFRASTRUCTURE_TEMPLATE)
INFRASTRUCTURE_STACK_ID = "example-stack"


### Environment Variables

#Enter the command used to call python from the cmd/terminal (ex: py, python, python3...)
PYTHON = 'python3'





