# 志愿项目自然语言处理系统

这是一个基于深度学习和自然语言处理技术的志愿项目查询系统，能够将用户的自然语言描述转化为标准格式，并在数据库中查找匹配的志愿项目。

## 功能特性

- **自然语言理解**: 支持中文自然语言输入
- **智能信息提取**: 自动提取年龄、人数、日期、时间、活动类型等信息
- **模糊匹配**: 处理各种表达方式，如"我和朋友"自动识别为2人
- **实时查询**: 基于提取的信息在数据库中查找匹配项目
- **Web API**: 提供RESTful接口供外部调用
- **智能验证**: 自动过滤无效日期和离谱人数（限制在50人以内）
- **交互询问**: 信息不完整时主动询问补充信息
- **日期限制**: 只能预约未来一年内的活动，自动过滤过去日期

## 技术栈

- **NLP引擎**: jieba分词 + 正则表达式 + 规则匹配
- **Web框架**: Flask
- **语言**: Python 3.6+

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行命令行版本

```bash
python volunteer_nlp_system.py
```

### 3. 启动Web服务

```bash
python volunteer_api.py
```

服务将在 http://localhost:5000 启动

## API接口

### 处理自然语言查询

**POST /api/process**

**请求示例:**
```json
{
  "text": "我和我朋友都是16岁，我和他要做一个在4月3号上午的志愿活动，我们想做环保类型的"
}
```

**响应示例:**
```json
{
  "processed_data": {
    "原始输入": "我和我朋友都是16岁，我和他要做一个在4月3号上午的志愿活动，我们想做环保类型的",
    "年龄": 16,
    "人数": 2,
    "日期": "2024-04-03",
    "时间": "08:00-12:00",
    "活动类型": "环保",
    "处理时间": "2024-04-01 10:30:00"
  },
  "query_conditions": {
    "activity_type": "环保",
    "date": "2024-04-03",
    "time_range": "08:00-12:00",
    "participants": 2,
    "age_limit": 16
  },
  "matched_projects": [
    {
      "id": 1,
      "name": "城市公园环保清洁行动",
      "type": "环保",
      "date": "2024-04-03",
      "time": "08:00-12:00",
      "age_limit": "12-60",
      "max_participants": 50,
      "description": "清理公园垃圾，宣传环保知识",
      "location": "市中心公园"
    }
  ],
  "project_count": 1
}
```

### 获取所有项目

**GET /api/projects**

### 运行测试用例

**GET /api/test**

## 使用示例

### 1. 命令行使用

```python
from volunteer_nlp_system import VolunteerNLPEngine

nlp = VolunteerNLPEngine()
result = nlp.process_natural_language("我和朋友想参加4月3号的环保活动，我们都是16岁")
print(result)
```

### 2. Web API使用

```python
import requests

response = requests.post('http://localhost:5000/api/process', 
                        json={'text': '我和朋友想参加4月3号的环保活动，我们都是16岁'})
print(response.json())
```

## 支持的表达方式

### 年龄
- "16岁"
- "16周岁"
- "年龄16"

### 人数
- "2个人"
- "我和朋友" → 2人
- "我和他们" → 3人
- "我一个人" → 1人

### 日期
- "4月3日"
- "4月3号"
- "4/3"
- "明天"
- "后天"

### 时间
- "上午" → 08:00-12:00
- "下午" → 14:00-18:00
- "8点到12点"
- "上午9点到11点"

### 活动类型
- 环保: 环保、垃圾分类、植树、清洁等
- 教育: 教育、教学、辅导、支教等
- 社区服务: 社区、敬老院、养老院等
- 医疗: 医疗、医院、健康、献血等

## 测试

运行单元测试:

```bash
python test_system.py
```

## 扩展开发

### 添加新的活动类型

在 `volunteer_nlp_system.py` 中的 `extract_activity_type` 方法里添加新的关键词。

### 扩展数据库

在 `VolunteerDatabase` 类中添加更多项目数据，或连接到真实数据库。

### 改进NLP引擎

- 集成深度学习模型（如BERT）
- 添加更多语义理解能力
- 支持更复杂的时间表达式
- 增加地点识别功能

## 项目结构

```
├── volunteer_nlp_system.py  # 主要的NLP处理引擎
├── volunteer_api.py         # Web API服务
├── test_system.py          # 测试脚本
├── requirements.txt        # 依赖包列表
└── README.md              # 项目文档
```

## 许可证

MIT License