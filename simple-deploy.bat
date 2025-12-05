@echo off
echo 🚀 Preparing backend for Render deployment...

REM Check if Git is available
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    echo 📥 Download from: https://git-scm.com/download/win
    exit /b 1
)

echo 🔄 Initializing Git repository...
git init
git add .
git commit -m "Initial commit for emotion detection backend"

echo ✅ Backend is ready for deployment!
echo 📋 Next steps:
echo 1. Create a GitHub repository
echo 2. Push this code to GitHub:
echo    git remote add origin YOUR_GITHUB_REPO_URL
echo    git push -u origin main
echo 3. Visit https://render.com/
echo 4. Create a new Web Service
echo 5. Connect your GitHub repository
echo 6. Configure with:
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn app:app
echo    - Environment: Python 3.9
echo 7. Deploy!

echo 🌐 After deployment, update your frontend API URL in:
echo - frontend\src\components\EmotionSummary.js
echo - frontend\src\components\EmotionHighlighter.js
echo - frontend\src\components\EmotionChart.js

pause