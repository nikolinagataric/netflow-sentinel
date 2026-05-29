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

variable "lambda_image_uri" {
  description = "Full ECR image URI for the Lambda container image."
  type        = string
}
