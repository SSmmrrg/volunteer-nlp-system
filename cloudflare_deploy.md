# Cloudflare部署指南

## ❗ 重要说明

Cloudflare目前**不直接支持**传统的Python Flask应用部署。Cloudflare主要提供：

### 1. Cloudflare Pages（静态网站）
- 适用于：纯前端应用（HTML/CSS/JS）
- 不适用：Python Flask后端

### 2. Cloudflare Workers（边缘计算）
- 适用于：JavaScript/TypeScript函数
- 不适用：Python Flask应用

## ✅ 替代方案

### 方案一：使用Cloudflare Tunnel（推荐）
将本地运行的Python应用通过Cloudflare Tunnel暴露到公网：

1. **安装Cloudflare Tunnel**
```bash
# 下载Cloudflare Tunnel
https://github.com/cloudflare/cloudflared/releases
```

2. **创建Tunnel**
```bash
cloudflared tunnel create volunteer-nlp
```

3. **配置Tunnel**
创建 `cloudflared.yml`：
```yaml
tunnel: volunteer-nlp
credentials-file: /path/to/credentials.json

ingress:
  - hostname: volunteer-nlp.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404
```

4. **运行Tunnel**
```bash
cloudflared tunnel run volunteer-nlp
```

### 方案二：使用Cloudflare + 其他平台
通过Cloudflare CDN加速其他平台的部署：

1. 先部署到 **Render.com** 或 **Railway.app**
2. 在Cloudflare添加域名
3. 配置DNS指向部署平台
4. 启用Cloudflare CDN加速

## 🚀 推荐的免费部署平台

由于Cloudflare限制，推荐使用以下免费平台：

| 平台 | 特点 | 部署地址 |
|------|------|----------|
| **Render.com** | 完全免费，无需信用卡 | `https://volunteer-nlp.onrender.com` |
| **Railway.app** | 免费额度充足 | `https://volunteer-nlp.up.railway.app` |
| **PythonAnywhere** | Python专用 | `https://username.pythonanywhere.com` |

## 📋 快速部署步骤

### 使用Render.com（3分钟完成）
1. 访问 https://render.com
2. 用GitHub登录
3. 点击 "New" → "Web Service"
4. 选择你的仓库
5. 配置：
   - Name: `volunteer-nlp`
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn volunteer_api:app`
6. 点击 "Create Web Service"

### 使用Railway.app（2分钟完成）
1. 访问 https://railway.app
2. 用GitHub登录
3. 点击 "New Project"
4. 选择你的GitHub仓库
5. 自动部署完成

## 🔧 配置文件已准备

项目已包含所有必要的部署文件：
- ✅ `Procfile` - Render部署配置
- ✅ `requirements.txt` - 依赖列表
- ✅ `render.yaml` - Render配置文件
- ✅ `railway.json` - Railway配置文件

## 🎯 总结

虽然Cloudflare不直接支持Python Flask应用，但你可以：

1. **使用Render.com** - 最简单、完全免费
2. **使用Railway.app** - 界面友好、免费额度充足
3. **使用Cloudflare Tunnel** - 将本地服务暴露到公网
4. **使用Cloudflare CDN** - 加速其他平台的访问

**推荐顺序**：Render.com → Railway.app → 其他平台

立即开始部署吧！