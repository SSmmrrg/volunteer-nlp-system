#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
志愿项目NLP系统 - 一键部署助手
"""

import os
import subprocess
import json

def create_render_config():
    """创建Render部署配置"""
    config = {
        "services": [
            {
                "type": "web",
                "name": "volunteer-nlp-system",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "gunicorn volunteer_api:app --bind 0.0.0.0:$PORT"
            }
        ]
    }
    
    with open('render.yaml', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 已创建render.yaml配置文件")

def create_railway_config():
    """创建Railway部署配置"""
    config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "gunicorn volunteer_api:app --bind 0.0.0.0:$PORT",
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open('railway.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 已创建railway.json配置文件")

def create_vercel_config():
    """创建Vercel部署配置"""
    config = {
        "version": 2,
        "builds": [
            {
                "src": "volunteer_api.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "volunteer_api.py"
            }
        ]
    }
    
    with open('vercel.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 已创建vercel.json配置文件")

def create_gitignore():
    """创建.gitignore文件"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✅ 已创建.gitignore文件")

def init_git_repo():
    """初始化Git仓库"""
    print("⚠️  请手动初始化Git仓库：")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")

def main():
    """主函数"""
    print("🚀 志愿项目NLP系统 - 一键部署助手")
    print("=" * 50)
    
    # 创建所有配置文件
    create_render_config()
    create_railway_config()
    create_vercel_config()
    create_gitignore()
    
    print("\n📋 手动部署步骤：")
    print("1. 在GitHub创建新仓库")
    print("2. 上传代码到GitHub：")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git remote add origin https://github.com/yourusername/volunteer-nlp-system.git")
    print("   git push -u origin main")
    print("3. 选择部署平台：")
    print("   - Render: https://render.com")
    print("   - Railway: https://railway.app")
    print("   - PythonAnywhere: https://www.pythonanywhere.com")
    print("4. 连接GitHub仓库并部署")
    
    print("\n🔗 部署完成后，您将获得类似：")
    print("   https://your-app-name.onrender.com")
    print("   https://your-app-name.up.railway.app")

if __name__ == "__main__":
    main()