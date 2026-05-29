resource "aws_sfn_state_machine" "pipeline" {
  count = var.deploy_lambda ? 1 : 0

  name     = "${local.name_prefix}-pipeline"
  role_arn = aws_iam_role.step_functions_role.arn

  definition = jsonencode({
    Comment = "Run the NetFlow Sentinel Lambda pipeline."
    StartAt = "RunNetFlowSentinelPipeline"
    States = {
      RunNetFlowSentinelPipeline = {
        Type     = "Task"
        Resource = aws_lambda_function.pipeline[0].arn
        End      = true
      }
    }
  })

  tags = {
    Project = var.project_name
  }
}
