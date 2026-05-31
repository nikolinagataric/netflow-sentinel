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

$RepositoryUri = "$AccountId.dkr.ecr.$Region.amazonaws.com/$RepositoryName"
$RemoteImageUri = "${RepositoryUri}:${ImageTag}"

Write-Host "Logging in to Amazon ECR..."
aws ecr get-login-password --region $Region |
    docker login --username AWS --password-stdin "$AccountId.dkr.ecr.$Region.amazonaws.com"

Write-Host "Building and pushing Lambda container image..."
docker buildx build `
    --platform linux/amd64 `
    --provenance=false `
    --sbom=false `
    -f Dockerfile.lambda `
    -t $RemoteImageUri `
    --push .

Write-Host "Image pushed: $RemoteImageUri"
