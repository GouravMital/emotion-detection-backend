@echo off
echo 🚀 Deploying backend to GitHub for Render deployment...

echo 📋 Please create a new GitHub repository first:
echo 1. Visit https://github.com/new
echo 2. Create repository named: emotion-detection-backend
echo 3. Copy the repository URL (HTTPS)
echo.

set /p repo_url="Enter your GitHub repository URL: "

echo 🔄 Adding remote repository...
git remote add origin %repo_url%

echo 📤 Pushing code to GitHub...
git push -u origin main

echo ✅ Backend code pushed to GitHub!
echo.
echo 🌐 Now deploying to Render...
echo 1. Visit https://render.com/
echo 2. Click "New Web Service"
echo 3. Connect your GitHub repository
echo 4. Configure:
echo    - Name: emotion-detection-backend
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn app:app
echo    - Environment: Python 3.9
echo 5. Click "Create Web Service"
echo.
echo 📝 After deployment, copy the deployed URL and update frontend config!
pause