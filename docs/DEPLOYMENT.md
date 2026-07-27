# 🚀 TeleGame Deployment Guide

## Deploying to Vercel Serverless

1. Install Vercel CLI or connect your GitHub repository to Vercel.
2. Configure Environment Variables in Vercel Project Settings:
   - `BOT_TOKEN`
   - `DATABASE_URL` (Use Supabase PostgreSQL URL with `postgresql+asyncpg://`)
   - `WEBHOOK_URL` (e.g. `https://your-app.vercel.app`)
3. Set Webhook:
   ```bash
   curl -F "url=https://your-app.vercel.app/webhook" https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook
   ```

## Deploying to Railway / Render / Docker
Deploy using the included `Dockerfile` or `docker-compose.yml`.
