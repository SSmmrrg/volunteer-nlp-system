#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from volunteer_nlp_system import VolunteerNLPEngine, VolunteerDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

nlp_engine = VolunteerNLPEngine()
database = VolunteerDatabase()

@app.route('/')
def index():
    """首页"""
    return """
    <html>
    <head>
        <title>志愿项目NLP系统</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 300;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .content {
                padding: 40px;
            }
            
            .section {
                margin-bottom: 30px;
            }
            
            .section h2 {
                color: #333;
                margin-bottom: 15px;
                font-size: 1.8em;
                border-left: 4px solid #4CAF50;
                padding-left: 15px;
            }
            
            .endpoint {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                margin: 15px 0;
            }
            
            .endpoint strong {
                color: #495057;
                font-size: 1.1em;
            }
            
            .example {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 10px;
                padding: 20px;
                margin: 15px 0;
                border-left: 4px solid #ffc107;
            }
            
            .form-container {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 30px;
                margin-top: 20px;
            }
            
            .form-title {
                font-size: 1.5em;
                color: #333;
                margin-bottom: 20px;
                text-align: center;
            }
            
            .input-group {
                margin-bottom: 20px;
            }
            
            .input-label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #495057;
            }
            
            textarea {
                width: 100%;
                min-height: 120px;
                padding: 15px;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                font-size: 16px;
                font-family: inherit;
                resize: vertical;
                transition: all 0.3s ease;
                background: white;
            }
            
            textarea:focus {
                outline: none;
                border-color: #4CAF50;
                box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
            }
            
            textarea::placeholder {
                color: #6c757d;
                font-style: italic;
            }
            
            .submit-btn {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                border: none;
                padding: 15px 40px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 50px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
                display: block;
                margin: 0 auto;
                min-width: 200px;
            }
            
            .submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
            }
            
            .submit-btn:active {
                transform: translateY(0);
                box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            
            .feature {
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .feature:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .feature-icon {
                font-size: 2em;
                margin-bottom: 10px;
            }
            
            @media (max-width: 600px) {
                .container {
                    margin: 10px;
                    border-radius: 15px;
                }
                
                .header, .content {
                    padding: 20px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌱 志愿项目智能匹配系统</h1>
                <p>用自然语言描述您的志愿需求，AI为您精准匹配</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>🚀 核心功能</h2>
                    <div class="features">
                        <div class="feature">
                            <div class="feature-icon">🗣️</div>
                            <h3>自然语言理解</h3>
                            <p>支持中文自然语言输入，无需专业术语</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">🎯</div>
                            <h3>智能信息提取</h3>
                            <p>自动识别年龄、人数、时间、活动类型</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">⚡</div>
                            <h3>实时项目匹配</h3>
                            <p>基于提取信息快速匹配相关志愿项目</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📋 API接口</h2>
                    <div class="endpoint">
                        <strong>POST /api/process</strong><br>
                        <small>处理自然语言查询，返回标准格式和匹配项目</small><br>
                        <code style="background: #e9ecef; padding: 2px 6px; border-radius: 3px;">{"text": "你的描述"}</code>
                    </div>
                </div>
                
                <div class="section">
                    <h2>💡 使用示例</h2>
                    <div class="example">
                        <strong>示例1:</strong> "我和我朋友都是16岁，我和他要做一个在4月3号上午的志愿活动，我们想做环保类型的"<br>
                        <small>→ 年龄: 16岁, 人数: 2人, 日期: 4月3日, 时间: 上午, 类型: 环保</small>
                    </div>
                    
                    <div class="example">
                        <strong>示例2:</strong> "我想一个人参加明天下午的社区服务活动，我18岁了"<br>
                        <small>→ 年龄: 18岁, 人数: 1人, 日期: 明天, 时间: 下午, 类型: 社区服务</small>
                    </div>
                </div>
                
                <div class="form-container">
                    <h3 class="form-title">🧪 在线测试</h3>
                    <form action="/api/process" method="post">
                        <div class="input-group">
                            <label class="input-label">描述您的志愿需求：</label>
                            <textarea name="text" placeholder="例如：我和朋友都是16岁，想在4月3号上午参加环保活动..." required></textarea>
                        </div>
                        <button type="submit" class="submit-btn">🚀 智能匹配</button>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/process', methods=['POST'])
def process_query():
    try:
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '')
        else:
            text = request.form.get('text', '')
            
        if not text:
            return jsonify({"error": "请提供文本输入"}), 400
            
        logger.info(f"收到查询: {text}")

        processed_data = nlp_engine.process_natural_language(text)

        query = nlp_engine.generate_database_query(processed_data)

        results = database.search_projects(query)

        response = {
            "processed_data": processed_data,
            "query_conditions": query,
            "matched_projects": results,
            "project_count": len(results)
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"处理查询时出错: {str(e)}")
        return jsonify({"error": f"处理失败: {str(e)}"}), 500

@app.route('/api/projects', methods=['GET'])
def get_all_projects():
    return jsonify({
        "projects": database.projects,
        "total_count": len(database.projects)
    })

@app.route('/api/test', methods=['GET'])
def run_tests():
    test_cases = [
        "我和我朋友都是16岁，我和他要做一个在4月3号上午的志愿活动，我们想做环保类型的",
        "我想一个人参加明天下午的社区服务活动，我18岁了",
        "我们三个人想在4月3号做一些环保相关的事情，都是大学生",
        "明天我想和朋友一起参加敬老院的志愿活动"
    ]
    
    results = []
    for text in test_cases:
        processed_data = nlp_engine.process_natural_language(text)
        query = nlp_engine.generate_database_query(processed_data)
        matched_projects = database.search_projects(query)
        
        results.append({
            "input": text,
            "processed_data": processed_data,
            "matched_projects": matched_projects,
            "project_count": len(matched_projects)
        })
    
    return jsonify({
        "test_results": results,
        "total_tests": len(test_cases)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)