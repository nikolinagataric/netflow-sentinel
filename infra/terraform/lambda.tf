resource "aws_lambda_function" "pipeline" {
  count = var.deploy_lambda ? 1 : 0

  function_name = "${local.name_prefix}-pipeline"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = var.lambda_image_uri
  timeout       = 900
  memory_size   = 3008

  environment {
    variables = {
      PROJECT_NAME = var.project_name
    }
  }

  tags = {
    Project = var.project_name
  }
}
