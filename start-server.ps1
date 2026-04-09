#!/usr/bin/env powershell
# Global Grant Intelligence Platform - Backend Server Starter
# This script ensures the server starts from the correct directory with the correct venv

$ErrorActionPreference = "Stop"

# Get the directory where this script is located
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BackendDir = Join-Path $RootDir "backend"
$VenvPath = Join-Path $BackendDir ".venv\Scripts"

# Verify backend directory exists
if (-not (Test-Path $BackendDir)) {
    Write-Error "ERROR: 'backend' directory not found at $BackendDir"
    exit 1
}

# Verify venv exists
if (-not (Test-Path $VenvPath)) {
    Write-Error "ERROR: Virtual environment not found at $VenvPath"
    Write-Host "Run: python -m venv backend\.venv"
    Write-Host "Then: backend\.venv\Scripts\pip install -r backend\requirements.txt"
    exit 1
}

# Start the server from the backend directory
Write-Host "Starting server from $BackendDir using venv at $VenvPath" -ForegroundColor Green
Write-Host "Server will be available at http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Change to backend directory and run uvicorn using absolute path
Set-Location $BackendDir
$UvicornPath = Join-Path $VenvPath "uvicorn.exe"
& $UvicornPath main:app --reload --host 0.0.0.0 --port 8000
