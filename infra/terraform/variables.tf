variable "region" {
  description = "AWS region where resources will be created."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "netflow-sentinel"
}

variable "bucket_name" {
  description = "S3 bucket name for input files and pipeline outputs. Must be globally unique."
  type        = string
}

variable "deploy_lambda" {
  description = "Whether to deploy Lambda and Step Functions resources. Set to false for the first Terraform apply, then true after the Lambda image is pushed to ECR."
  type        = bool
  default     = false
}

variable "lambda_image_uri" {
  description = "Full ECR image URI for the Lambda container image. Required when deploy_lambda is true."
  type        = string
  default     = ""
}
