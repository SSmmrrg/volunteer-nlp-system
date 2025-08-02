#!/usr/bin/env python3
"""
Cloudflare Tunnel 设置助手
用于将本地Python应用通过Cloudflare暴露到公网
"""

import os
import json

def create_tunnel_config():
    """创建Cloudflare Tunnel配置"""
    
    print("🌐 Cloudflare Tunnel 设置指南")
    print("=" * 40)
    
    print("\n❗ Cloudflare不直接支持Python Flask应用")
    print("✅ 但可以通过 Cloudflare Tunnel 将本地服务暴露到公网")
    
    print("\n📋 步骤1：安装 Cloudflared")
    print("   Windows: https://github.com/cloudflare/cloudflared/releases")
    print("   下载 cloudflared-windows-amd64.exe")
    
    print("\n📋 步骤2：创建隧道")
    print("   cloudflared tunnel create volunteer-nlp")
    
    print("\n📋 步骤3：运行本地服务")
    print("   python volunteer_api.py")
    
    print("\n📋 步骤4：启动隧道")
    print("   cloudflared tunnel --url http://localhost:5000")
    
    print("\n📋 步骤5：获得公网地址")
    print("   隧道会提供类似：https://volunteer-nlp.trycloudflare.com")
    
    print("\n🎯 更简单的方法：")
    print("   使用 Render.com 或 Railway.app 直接部署")
    print("   然后使用 Cloudflare CDN 加速")
    
    # 创建简单的批处理文件
    bat_content = """@echo off
echo 启动 Cloudflare Tunnel...
echo 请确保本地服务已运行：python volunteer_api.py
echo.
cloudflared tunnel --url http://localhost:5000
pause
"""
    
    with open('start_tunnel.bat', 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    print("\n✅ 已创建 start_tunnel.bat 一键启动脚本")
    print("   双击即可启动 Cloudflare Tunnel")

if __name__ == "__main__":
    create_tunnel_config()