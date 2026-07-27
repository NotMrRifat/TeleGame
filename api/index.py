"""Vercel Serverless ASGI Entrypoint."""

from app.main import app

# Vercel handles app automatically via ASGI
__all__ = ["app"]
