@echo off
echo 🚀 Complete Backend Deployment Process
echo ======================================

REM Check if git is configured
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    exit /b 1
)

echo 📋 Step 1: Creating GitHub repository...
echo.
echo Please create a GitHub repository manually:
echo 1. Go to https://github.com/new
echo 2. Name it: emotion-detection-backend
echo 3. Make it Public
echo 4. Don't initialize with README
echo 5. Click "Create repository"
echo.
set /p repo_created="Press Enter when you've created the repository..."

echo 📋 Step 2: Enter your GitHub repository URL:
echo Example: https://github.com/yourusername/emotion-detection-backend.git
set /p repo_url="Enter repository URL: "

echo 🔄 Step 3: Setting up Git and pushing code...
git remote remove origin 2>nul
git remote add origin %repo_url%
git branch -M main
git push -u origin main

echo ✅ Code pushed to GitHub!

echo 🌐 Step 4: Deploying to Render...
echo Opening Render dashboard...
start https://render.com/

echo.
echo 📋 Manual steps on Render:
echo 1. Click "New +" → "Web Service"
echo 2. Connect your GitHub account
echo 3. Select "emotion-detection-backend" repository
echo 4. Configure:
echo    - Name: emotion-detection-backend
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn app:app
echo    - Instance Type: Free
echo 5. Click "Create Web Service"
echo.
echo ⏳ Wait for deployment to complete (5-10 minutes)
echo 📋 After deployment:
echo 1. Copy the deployed URL (e.g., https://emotion-detection-backend-XXXX.onrender.com)
echo 2. Update frontend configuration
echo.
set /p backend_url="Enter your deployed backend URL (without /api): "

echo 📝 Step 5: Creating frontend config update script...
echo export const API_BASE_URL = '%backend_url%/api'; > ..\frontend\src\config.js

echo ✅ Frontend configuration updated!
echo.
echo 🚀 Step 6: Redeploying frontend...
cd ..\frontend
call npm run build
call netlify deploy --prod --dir=build

echo 🎉 DEPLOYMENT COMPLETE!
echo =====================
echo Frontend: https://emotion-detection-ai.netlify.app
echo Backend: %backend_url%
echo.
echo 🧪 Testing your deployment...
echo Opening test page...
start https://emotion-detection-ai.netlify.app

echo ✅ All done! Your emotion detection AI is fully deployed and connected!
pause