# Deploy Workflow Setup Guide

This guide explains how to configure GitHub Secrets for the deployment workflow.

## Required GitHub Secrets

You need to set up the following secrets in your GitHub repository:

1. **KEY** - Your AWS Lightsail private key content
2. **SSH_USER** - SSH username 
3. **SSH_HOST** - Server IP address

## How to Set Up GitHub Secrets

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click on **Secrets and variables** → **Actions**
4. Click on **New repository secret**
5. Add each secret:

### LIGHTSAIL_SSH_KEY
- **Name**: `KEY`
- **Value**: Copy the entire content of your `.pem` file, including:
  ```
  -----BEGIN RSA PRIVATE KEY-----
  [Your key content here]
  -----END RSA PRIVATE KEY-----
  ```

### SSH_USER
- **Name**: `SSH_USER`

### SSH_HOST
- **Name**: `SSH_HOST`

## How to Run the Deployment

1. Go to the **Actions** tab in your GitHub repository
2. Select **Deploy to Lightsail Server** workflow
3. Click **Run workflow**
4. Select the branch (usually `main`)
5. Click **Run workflow** button

The workflow will:
- Connect to your Lightsail server using SSH
- Navigate to the `toko` directory
- Pull the latest changes from GitHub
- Stop and remove the existing Docker container
- Build a new Docker image
- Start a new container with the environment variables from `.env` file

## Prerequisites on Server

Make sure your Lightsail server has:
- Docker installed
- Git repository cloned in the `toko` directory
- `.env` file with Discord bot configuration in the `toko` directory
