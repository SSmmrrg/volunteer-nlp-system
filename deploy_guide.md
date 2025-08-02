# 志愿项目NLP系统 - 免费部署指南

## 🚀 免费部署方案

本指南将帮助您将志愿项目NLP系统免费部署到公网，让任何人都可以访问。

## 方案一：Render.com (推荐)

### 步骤1：准备项目
1. 确保项目文件完整：
   - `volunteer_nlp_system.py`
   - `volunteer_api.py`
   - `requirements.txt`

### 步骤2：创建部署文件

#### 创建 `render.yaml`
```yaml
services:
  - type: web
    name: volunteer-nlp-system
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python volunteer_api.py
    envVars:
      - key: PORT
        value: 10000
```

#### 创建 `.gitignore`
```
__pycache__/
*.pyc
.env
venv/
```

### 步骤3：部署到Render
1. 访问 [https://render.com](https://render.com)
2. 注册账号（支持GitHub登录）
3. 创建新的Web Service
4. 连接GitHub仓库
5. 选择项目并部署

## 方案二：Railway.app

### 步骤1：创建 `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python volunteer_api.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 步骤2：部署到Railway
1. 访问 [https://railway.app](https://railway.app)
2. 注册账号
3. 创建新项目
4. 从GitHub导入代码
5. 自动部署

## 方案三：PythonAnywhere

### 步骤1：注册账号
1. 访问 [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. 注册免费账号

### 步骤2：上传代码
1. 登录控制面板
2. 进入"Files"标签页
3. 上传项目文件
4. 创建虚拟环境：
   ```bash
   mkvirtualenv volunteer-nlp --python=/usr/bin/python3.8
   pip install -r requirements.txt
   ```

### 步骤3：配置Web应用
1. 进入"Web"标签页
2. 创建新的Web应用
3. 选择Flask框架
4. 配置WSGI文件

## 方案四：Heroku (需信用卡验证)

### 步骤1：创建必要文件

#### 创建 `Procfile`
```
web: python volunteer_api.py
```

#### 创建 `runtime.txt`
```
python-3.8.10
```

### 步骤2：部署到Heroku
1. 安装Heroku CLI
2. 登录Heroku: `heroku login`
3. 创建应用: `heroku create volunteer-nlp-system`
4. 部署: `git push heroku main`

## 方案五：Vercel (前端部署)

### 步骤1：创建简化版本
创建 `vercel.json`:
```json
{
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
```

## 部署前检查清单

### 代码调整
确保 `volunteer_api.py` 中的以下配置：
```python
# 修改为环境变量读取端口
import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
```

### 依赖检查
确保 `requirements.txt` 包含所有必要依赖：
```
flask>=2.0.0
jieba>=0.42.1
gunicorn>=20.1.0  # 添加这个用于生产环境
```

### 生产环境配置
创建 `wsgi.py`:
```python
from volunteer_api import app

if __name__ == "__main__":
    app.run()
```

## 部署步骤总结

### 1. 选择平台
- **Render**: 最简单，推荐
- **Railway**: 现代化界面
- **PythonAnywhere**: Python专用
- **Heroku**: 传统选择

### 2. 准备代码
```bash
git init
git add .
git commit -m "Initial commit"
```

### 3. 推送到GitHub
```bash
git remote add origin https://github.com/yourusername/volunteer-nlp-system.git
git push -u origin main
```

### 4. 部署
按照所选平台的步骤进行部署

## 部署后访问

部署成功后，您将获得类似以下的公网URL：
- `https://volunteer-nlp-system.onrender.com`
- `https://volunteer-nlp-system.up.railway.app`
- `https://yourusername.pythonanywhere.com`

## 测试部署

### 使用curl测试
```bash
curl -X POST https://your-app-url.com/api/process \
  -H "Content-Type: application/json" \
  -d '{"text":"我和朋友都是16岁，想在4月3号上午参加环保活动"}'
```

### 浏览器测试
直接访问部署的URL，使用网页表单进行测试

## 常见问题解决

### 端口问题
确保使用环境变量读取端口：
```python
port = int(os.environ.get("PORT", 5000))
```

### 依赖问题
确保所有依赖都在 `requirements.txt` 中

### 内存限制
免费计划通常有512MB内存限制，本项目完全够用

## 监控和维护

### 查看日志
各平台都提供日志查看功能：
- Render: Dashboard → Logs
- Railway: Dashboard → Logs
- PythonAnywhere: Web tab → Log files

### 更新代码
每次代码更新后，平台会自动重新部署

## 联系方式
如有部署问题，请通过GitHub Issues联系

---
**推荐顺序**: Render → Railway → PythonAnywhere → Heroku