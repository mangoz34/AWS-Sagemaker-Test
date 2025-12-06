from sagemaker import Model
from sagemaker.workflow.model_step import ModelStep

# Get the Linear Learner container for inference
container_image_uri = sagemaker.image_uris.retrieve(framework="linear-learner", region=region)

# Create model object referencing the training step output
model = Model(image_uri=container_image_uri,
              model_data=step_training.properties.ModelArtifacts.S3ModelArtifacts,
              sagemaker_session=pipeline_session, role=role,)

# Configure model registration
model_approval_status = "PendingManualApproval"
customer_metadata_properties = {"ModelType": "EmpBonusPrediction"}
register_args = model.register(content_types=["text/csv"],
                               response_types=["text/csv"],
                               inference_instances=["ml.t2.medium", "ml.m5.xlarge"],
                               transform_instances=["ml.m5.xlarge"],
                               model_package_group_name=model_package_group_name,
                               approval_status=model_approval_status,
                               customer_metadata_properties=customer_metadata_properties,)
step_register = ModelStep(name="RegisterModelEmpBonus", step_args=register_args)
