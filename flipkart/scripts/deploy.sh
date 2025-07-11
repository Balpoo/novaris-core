#!/bin/bash
echo "🚀 Deploying Flipkart Project"
git init
git add .
git commit -m "🚀 Phase 2: Flipkart Agents Initialized"
git remote add origin https://github.com/YOUR_USERNAME/flipkart-novaris.git
git push -u origin main
vercel --prod
