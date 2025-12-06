import boto3
import pandas as pd
import sagemaker
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.parameters import (ParameterInteger, ParameterString)
s3_client = boto3.resource('s3')

# The name of our eventual pipeline 
my_inits = 'ahs'  # TODO: Put YOUR initials here!!!
pipeline_name = f"bonus-training-pipeline-{my_inits}"

# Uses our current Sagemaker session
sagemaker_session = sagemaker.Session()
region = sagemaker_session.boto_region_name
role = sagemaker.get_execution_role()
pipeline_session = PipelineSession()
default_bucket = sagemaker_session.default_bucket()  # Default S3 bucket for data
model_package_group_name = f"BonusPackageGroup-{my_inits}"  # Name of the registered model group

# Print out our details so we can confirm in the AWS UI
print(f"Default S3 Bucket Name: {default_bucket}")
print(f"Model Package Group Name: {model_package_group_name}")
