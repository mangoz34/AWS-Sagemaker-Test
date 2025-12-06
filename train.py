from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep

# Retrieve the Linear Learner container image
linear_learner_container = sagemaker.image_uris.retrieve('linear-learner', sagemaker_session.boto_region_name)

# Configure the Linear Learner estimator
linear_estimator = Estimator(image_uri=linear_learner_container,
                             role=role, instance_count=1,
                             instance_type=training_instance_type,
                             output_path=f's3://{default_bucket}/model-output',
                             sagemaker_session=pipeline_session,
                             base_job_name="emp-bonus-linear-learner")

# Set hyperparameters for regression
linear_estimator.set_hyperparameters(predictor_type='regressor',
                                     mini_batch_size=32, epochs=10)

# Define training data inputs
train_path = f"s3://{default_bucket}/output/train/train.csv"
val_path = f"s3://{default_bucket}/output/validation/validation.csv"
train_input = TrainingInput(s3_data=train_path, content_type='text/csv')
val_input = TrainingInput(s3_data=val_path, content_type='text/csv')

# Create the training step
step_training = TrainingStep(name="TrainingEmpBonus",
                             estimator=linear_estimator,
                             inputs={'train': train_input,
                                     'validation': val_input},
                             depends_on=[step_data_split])
