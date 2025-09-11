# Git Repository Setup Guide

## Complete Steps to Create GitHub Repository and Push Code

### 1. Initialize Git Repository
```bash
git init
```
**What it does:** Creates a new Git repository in your current directory, initializing the `.git` folder that tracks all changes.

### 2. Create .gitignore File
```bash
echo "env/" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
```
**What it does:** Creates a `.gitignore` file to exclude sensitive files (like your API key) and unnecessary files from being tracked by Git.

### 3. Add Files to Git
```bash
git add .
```
**What it does:** Stages all files in your directory for the first commit (except those in `.gitignore`).

### 4. Make Initial Commit
```bash
git commit -m "Initial commit: Gemini image analysis tool"
```
**What it does:** Creates the first commit with all your staged files and a descriptive message.

### 5. Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon → "New repository"
3. Name your repository (e.g., "gemini-image-analyzer")
4. Keep it **Public** or **Private** (your choice)
5. **Don't** initialize with README, .gitignore, or license (since you already have files)
6. Click "Create repository"

### 6. Connect Local Repository to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```
**What it does:** Links your local Git repository to the GitHub repository you just created.

### 7. Push Code to GitHub
```bash
git branch -M main
git push -u origin main
```
**What it does:** 
- `git branch -M main`: Renames your default branch to "main"
- `git push -u origin main`: Uploads your code to GitHub and sets up tracking

### 8. Verify Upload
Go to your GitHub repository page to see your files uploaded successfully.

## 9. Remove Sensitive Files from Git (If Already Committed)

### If config.env is already tracked:
```bash
git rm --cached env/config.env
echo "env/config.env" >> .gitignore
git add .gitignore
git commit -m "Remove config.env from tracking and add to .gitignore"
git push
```
**What it does:** Removes the sensitive file from Git tracking while keeping it locally, adds it to `.gitignore`, and pushes the changes.

### Alternative: Remove entire env/ folder
```bash
git rm -r --cached env/
echo "env/" >> .gitignore
git add .gitignore
git commit -m "Remove env/ folder from tracking and add to .gitignore"
git push
```
**What it does:** Removes the entire `env/` folder from Git tracking and adds it to `.gitignore`.

### Verify sensitive files are no longer tracked:
```bash
git status
```
**What it does:** Shows that sensitive files are no longer being tracked by Git.

## Important Notes:
- **Never commit API keys**: Make sure your `.gitignore` excludes the `env/` folder where your API key is stored
- **Repository name**: Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and chosen repository name
- **Authentication**: You might need to authenticate with GitHub (using a personal access token or SSH key)

## Quick Reference Commands:
```bash
git init
echo "env/" > .gitignore && echo "*.pyc" >> .gitignore && echo "__pycache__/" >> .gitignore && echo ".env" >> .gitignore
git add .
git commit -m "Initial commit: Gemini image analysis tool"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```
