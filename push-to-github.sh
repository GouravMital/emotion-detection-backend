#!/bin/bash

echo "Pushing backend code to GitHub..."
echo ""
echo "Please enter your GitHub repository URL:"
echo "Example: https://github.com/YOUR_USERNAME/emotion-detection-backend.git"
echo ""

read -p "Enter repository URL: " REPO_URL

echo "Adding all files..."
git add .

echo "Committing files..."
git commit -m "Initial commit: Emotion Detection Backend with Flask, BERT, and Gemini AI"

echo "Adding remote origin..."
git remote add origin $REPO_URL

echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Backend code pushed to GitHub successfully!"
echo "Now you can deploy to Render."
echo ""
read -p "Press Enter to continue..."