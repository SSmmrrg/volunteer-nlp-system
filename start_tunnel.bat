@echo off
echo 启动 Cloudflare Tunnel...
echo 请确保本地服务已运行：python volunteer_api.py
echo.
cloudflared tunnel --url http://localhost:5000
pause
