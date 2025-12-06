from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep

framework_version = "1.0-1"

base_job_prefix = "emp-bonus"
processing_instance_count = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
processing_instance_type = ParameterString(name="ProcessingInstanceType", default_value="ml.t3.medium")
training_instance_type = ParameterString(name="TrainingInstanceType", default_value="ml.m5.xlarge")
input_data = "data/mock_data.csv"
model_approval_status = ParameterString(name="ModelApprovalStatus", default_value="PendingManualApproval")

# Define SKLearnProcessor
sklearn_processor = SKLearnProcessor(
    framework_version=framework_version,
    instance_type=processing_instance_type,
    instance_count=processing_instance_count,
    base_job_name="pre-processing-emp-bonus",
    role=role,
    sagemaker_session=pipeline_session,
)

# Specify args for the processor
processor_args = sklearn_processor.run(
    inputs=[ProcessingInput(source=input_data,
                            destination="/opt/ml/processing/input"),],
    outputs=[ProcessingOutput(output_name="processed-data",
                              source='/opt/ml/processing/output',
                              destination=f"s3://{default_bucket}/output/processed")],
    code=f"preprocessing_script.py",
)

# Create the pre-processing step to eventually put in the pipeline
step_preprocess = ProcessingStep(name="PreProcessingEmpBonus", step_args=processor_args)

# This step reads the output from preprocessing and creates train/validation/test splits
input_data = f"s3://{default_bucket}/output/processed/transformed_data.csv"
sklearn_processor = SKLearnProcessor(framework_version=framework_version,
                                     instance_type=processing_instance_type,
                                     instance_count=processing_instance_count,
                                     base_job_name="emp-data-split", role=role,
                                     sagemaker_session=pipeline_session,)

processor_args = sklearn_processor.run(
    inputs=[ProcessingInput(source=input_data, destination="/opt/ml/processing/input"),],
    outputs=[ProcessingOutput(output_name="train",
                              source="/opt/ml/processing/train",
                              destination=f"s3://{default_bucket}/output/train"),
             ProcessingOutput(output_name="validation",
                              source="/opt/ml/processing/validation",
                              destination=f"s3://{default_bucket}/output/validation"),
             ProcessingOutput(output_name="test",
                              source="/opt/ml/processing/test",
                              destination=f"s3://{default_bucket}/output/test")],
    code=f"model_training_script.py",)

step_data_split = ProcessingStep(name="DataSplitEmpBonus", step_args=processor_args, depends_on=[step_preprocess])
