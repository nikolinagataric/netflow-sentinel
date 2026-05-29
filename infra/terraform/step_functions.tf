resource "aws_sfn_state_machine" "pipeline" {
  name     = "${local.name_prefix}-pipeline"
  role_arn = aws_iam_role.step_functions_role.arn

  definition = jsonencode({
    Comment = "Run the NetFlow Sentinel Lambda pipeline."
    StartAt = "RunNetFlowSentinelPipeline"
    States = {
      RunNetFlowSentinelPipeline = {
        Type     = "Task"
        Resource = aws_lambda_function.pipeline.arn
        End      = true
      }
    }
  })

  tags = {
    Project = var.project_name
  }
}
