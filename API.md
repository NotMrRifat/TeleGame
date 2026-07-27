# 🔌 TeleGame API & Webhook Reference

TeleGame exposes HTTP ASGI endpoints via FastAPI.

## Endpoints

### `GET /`
Returns root platform metadata and environment status.
```json
{
  "status": "online",
  "app": "TeleGame",
  "version": "1.0.0",
  "environment": "development"
}
```

### `GET /health`
Liveness health check endpoint returning platform uptime.

### `GET /readiness`
Readiness check verifying database connectivity. Returns HTTP 200 `{"status": "ready"}` or HTTP 503 if DB is unready.

### `GET /metrics`
System metrics returning loaded game plugins and active runtime statistics.

### `POST /webhook`
Telegram Bot Webhook endpoint handling incoming Telegram updates.

### `GET /api/cron/cleanup`
Serverless Lazy Timer cron endpoint. Triggered by GitHub Actions or Vercel Cron to clean up expired sessions without needing long-running background tasks.
