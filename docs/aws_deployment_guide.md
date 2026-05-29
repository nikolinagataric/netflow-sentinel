# AWS Deployment Guide

This document describes the planned AWS deployment flow for NetFlow Sentinel.

The project includes deployment-ready files, but the deployment should only be run after the AWS account, billing setup, and permissions are ready.

## Important Warnings

- Do not commit AWS credentials.
- Do not commit access keys, secret keys, account IDs, ARNs, or other private values.
- Do not run `terraform apply` until the AWS account and billing setup are ready.
- Review all Terraform resources before creating them.

## Planned Architecture

```text
S3 input/output bucket
-> AWS Lambda container image
-> Step Functions state machine
-> Terraform infrastructure as code
```

## Prerequisites

- verified AWS account
- AWS Budget alert
- AWS CLI v2 installed
- Terraform installed
- Docker installed
- `aws configure` completed locally

## Deployment Plan

### 1. Create or Check AWS Budget

Before creating infrastructure, create an AWS Budget alert in the AWS Console. This helps avoid unexpected costs while testing.

### 2. Configure AWS CLI

Configure the AWS CLI locally:

```powershell
aws configure
```

Use an IAM user or role with only the permissions needed for this project.

### 3. Phase 1: Initialize Terraform

From the Terraform folder:

```powershell
cd infra/terraform
terraform init
```

### 4. Phase 1: Create S3 and ECR

The first apply creates the S3 bucket and ECR repository only. Lambda and Step Functions are not created yet because the Lambda image does not exist in ECR.

Review the plan:

```powershell
terraform plan -var="bucket_name=your-unique-bucket-name"
```

Apply only when the AWS account and billing setup are ready:

```powershell
terraform apply -var="bucket_name=your-unique-bucket-name"
```

This creates S3 and ECR, but not Lambda or Step Functions.

### 5. Phase 2: Build and Push Lambda Image

After the ECR repository exists, build and push the Lambda image.

Template script:

```powershell
.\scripts\aws_build_and_push.ps1 `
  -Region "eu-central-1" `
  -AccountId "<your-account-id>" `
  -RepositoryName "netflow-sentinel-lambda" `
  -ImageTag "latest"
```

Use the pushed image URI as the `lambda_image_uri` Terraform variable.

### 6. Phase 3: Deploy Lambda and Step Functions

After the image is pushed to ECR, run Terraform again with `deploy_lambda=true` and the full image URI.

Review the plan:

```powershell
terraform plan -var="bucket_name=your-unique-bucket-name" -var="deploy_lambda=true" -var="lambda_image_uri=YOUR_ECR_IMAGE_URI"
```

Apply only when the plan looks correct:

```powershell
terraform apply -var="bucket_name=your-unique-bucket-name" -var="deploy_lambda=true" -var="lambda_image_uri=YOUR_ECR_IMAGE_URI"
```

### 7. Upload CICIDS2017 Sample CSV to S3

Upload a CSV file to the S3 bucket, for example:

```text
raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
```

### 8. Start Step Functions Execution

Example execution input:

```json
{
  "input_bucket": "bucket-name",
  "input_key": "raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
  "output_bucket": "bucket-name",
  "output_prefix": "runs/ddos-test",
  "max_rows": 50000,
  "train_model": true
}
```

### 9. Check Outputs in S3

Expected output layout:

```text
runs/ddos-test/processed/
runs/ddos-test/reports/
runs/ddos-test/models/
```

The `models/` folder is only created when `train_model` is true.

### 10. Cleanup

When testing is finished, destroy the Terraform-managed infrastructure:

```powershell
terraform destroy
```

Also check the AWS Console for any remaining manually created objects or uploaded data.
