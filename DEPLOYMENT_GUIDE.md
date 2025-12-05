# Backend Deployment Guide

## Cloud Deployment Options

### Option 1: Render (Recommended - Free Tier)

1. **Create Render Account**
   - Visit https://render.com/
   - Sign up for a free account

2. **Deploy via GitHub (Recommended)**
   - Push your backend code to GitHub
   - Connect GitHub repository to Render
   - Configure build settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Environment: Python 3.9

3. **Environment Variables**
   - Add any required environment variables in Render dashboard
   - Set `FLASK_ENV=production` for production mode

### Option 2: Railway (Free Tier)

1. **Create Railway Account**
   - Visit https://railway.app/
   - Sign up for free account

2. **Deploy from GitHub**
   - Connect GitHub repository
   - Railway will auto-detect Python app
   - Deploy automatically

### Option 3: Heroku (Free Tier)

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Create Heroku App**
   ```bash
   heroku create emotion-detection-backend
   heroku buildpacks:add heroku/python
   ```

3. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Environment Configuration

### Required Environment Variables
```
FLASK_ENV=production
PORT=5000 (auto-set by cloud provider)
```

### Optional Environment Variables
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Deployment Files

### Files Created for Deployment
- `Procfile` - Defines how to start the application
- `runtime.txt` - Specifies Python version
- `render.yaml` - Render deployment configuration
- `requirements.txt` - Updated with gunicorn

## Post-Deployment Steps

1. **Test Backend Health**
   ```bash
   curl https://your-backend-url.com/api/health
   ```

2. **Update Frontend API Endpoints**
   - Replace `http://localhost:5000` with your deployed backend URL
   - Update in frontend configuration files

3. **Enable CORS**
   - Backend already has CORS enabled for all origins
   - No additional configuration needed

## Troubleshooting

### Common Issues
1. **Memory Issues**: Large ML models may exceed free tier limits
2. **Build Timeouts**: Model loading takes time on first request
3. **Cold Starts**: First request after deployment may be slow

### Solutions
- Consider using smaller models for free tier deployment
- Implement health checks to keep app warm
- Use paid tiers for better performance

## Performance Optimization

### For Production
- Use environment variables for sensitive data
- Implement proper logging
- Add error monitoring (e.g., Sentry)
- Consider using a CDN for static assets
- Implement rate limiting for API endpoints

## Security Considerations

- Never commit API keys to code
- Use HTTPS in production
- Implement proper input validation
- Add rate limiting to prevent abuse
- Monitor for unusual activity

## Monitoring

- Set up application monitoring
- Track API response times
- Monitor error rates
- Set up alerts for downtime