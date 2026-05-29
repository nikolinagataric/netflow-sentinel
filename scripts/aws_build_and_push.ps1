param(
    [Parameter(Mandatory = $true)]
    [string]$Region,

    [Parameter(Mandatory = $true)]
    [string]$AccountId,

    [Parameter(Mandatory = $true)]
    [string]$RepositoryName,

    [Parameter(Mandatory = $false)]
    [string]$ImageTag = "latest"
)

$ErrorActionPreference = "Stop"

$LocalImageName = "netflow-sentinel-lambda"
$RepositoryUri = "$AccountId.dkr.ecr.$Region.amazonaws.com/$RepositoryName"
$RemoteImageUri = "${RepositoryUri}:${ImageTag}"

Write-Host "Logging in to Amazon ECR..."
aws ecr get-login-password --region $Region |
    docker login --username AWS --password-stdin "$AccountId.dkr.ecr.$Region.amazonaws.com"

Write-Host "Building Lambda container image..."
docker build -f Dockerfile.lambda -t $LocalImageName .

Write-Host "Tagging image as $RemoteImageUri..."
docker tag "${LocalImageName}:latest" $RemoteImageUri

Write-Host "Pushing image to ECR..."
docker push $RemoteImageUri

Write-Host "Image pushed: $RemoteImageUri"
