@echo off
echo 🚀 Starting Render deployment process...

REM Check if Git is available
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    exit /b 1
)

echo 📦 Installing Render CLI...
npm install -g @render/cli

echo 🔄 Initializing Git repository...
git init
git add .
git commit -m "Initial commit for emotion detection backend"

echo 🌐 Deploying to Render...
echo Please visit: https://render.com/
echo 1. Create a new Web Service
echo 2. Connect your GitHub repository or use Git
echo 3. Configure with:
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn app:app
echo    - Environment: Python 3.9
echo 4. Add environment variables if needed

echo ✅ Backend deployment setup complete!
echo 📝 Next steps:
echo 1. Visit https://render.com/
echo 2. Create a new Web Service
echo 3. Deploy your backend
echo 4. Update frontend API endpoints