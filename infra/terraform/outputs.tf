output "s3_bucket_name" {
  description = "S3 bucket used for pipeline input and output artifacts."
  value       = aws_s3_bucket.pipeline_artifacts.bucket
}

output "ecr_repository_url" {
  description = "ECR repository URL for the Lambda image."
  value       = aws_ecr_repository.lambda_image.repository_url
}

output "lambda_function_name" {
  description = "Lambda function name."
  value       = var.deploy_lambda ? aws_lambda_function.pipeline[0].function_name : null
}

output "step_function_arn" {
  description = "Step Functions state machine ARN."
  value       = var.deploy_lambda ? aws_sfn_state_machine.pipeline[0].arn : null
}
