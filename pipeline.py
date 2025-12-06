from sagemaker.workflow.pipeline import Pipeline

pipeline = Pipeline(name=pipeline_name,
                    parameters=[processing_instance_count,
                                processing_instance_type,
                                training_instance_type,
                                model_approval_status,
                                input_data,],
                    steps=[step_preprocess, step_data_split,
                           step_training, step_register],)

# Create or update the pipeline
pipeline.upsert(role_arn=role)
