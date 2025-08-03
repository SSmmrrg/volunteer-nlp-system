#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)

class LLMVolunteerNLPEngine:
    def __init__(self, model_type: str = "local", model_endpoint: str = None):
        """
        Args:
            model_type: "local" (本地模型) 或 "api" (云端API)
            model_endpoint: 模型服务地址
        """
        self.model_type = model_type
        self.model_endpoint = model_endpoint or "http://localhost:8000/v1/chat/completions"
        self.current_year = datetime.now().year
        self.current_date = datetime.now().date()
        self.max_future_days = 365
        self.max_people_count = 50
        self.activity_mapping = {
            "环保": ["环保", "环境保护", "垃圾分类", "植树", "绿化", "清洁", "捡垃圾", "保护地球", "绿色", "生态", "可持续发展", "低碳", "节能"],
            "教育": ["教育", "教学", "辅导", "支教", "培训", "学习", "读书", "知识", "图书馆"],
            "社区服务": ["社区", "敬老院", "养老院", "孤儿院", "福利", "关爱", "陪伴", "帮助", "服务", "志愿", "公益"],
            "医疗": ["医疗", "医院", "健康", "献血", "义诊", "救助", "护理"],
            "动物保护": ["动物", "流浪动物", "救助", "宠物", "保护", "关爱动物"]
        }
        
    def _build_prompt(self, text: str) -> str:
        prompt = f"""
        你是一个志愿活动信息提取专家，请从以下用户输入中提取关键信息，并以JSON格式返回。
        
        用户输入：{text}
        
        需要提取的信息：
        1. 年龄：用户的年龄（数字，如果没有则返回null）
        2. 人数：参与活动的总人数（数字，默认为1）
        3. 日期：希望参加活动的具体日期（格式：YYYY-MM-DD，如果没有则返回null）
        4. 时间：希望参加活动的具体时间段（如"上午"、"下午"、"09:00-12:00"等，如果没有则返回null）
        5. 活动类型：希望参加的活动类型（如"环保"、"教育"、"社区服务"、"医疗"、"动物保护"等，如果没有则返回"综合"）
        
        请严格按照以下JSON格式返回：
        {{
            "年龄": 数字或null,
            "人数": 数字,
            "日期": "YYYY-MM-DD"或null,
            "时间": "时间段字符串"或null,
            "活动类型": "活动类型字符串"
        }}
        
        注意：
        - 如果用户说"我和朋友"，人数应该是2
        - 如果用户说"4月3号"，假设年份是当前年份，如果日期已过则使用下一年
        - 时间段的表达要标准化，如"上午"→"08:00-12:00"，"下午"→"14:00-18:00"
        - 活动类型要从预定义类型中选择最接近的
        """
        return prompt.strip()
    
    def _call_local_model(self, prompt: str) -> Dict[str, Any]:
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "qwen-6b-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 200
            }
            
            response = requests.post(self.model_endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {}
                
        except Exception as e:
            logger.error(f"调用本地模型失败: {e}")
            return {}
    
    def _fallback_rule_based(self, text: str) -> Dict[str, Any]:
        from volunteer_nlp_system import VolunteerNLPEngine
        fallback_engine = VolunteerNLPEngine()
        
        return {
            "年龄": fallback_engine.extract_age(text),
            "人数": fallback_engine.extract_people_count(text),
            "日期": fallback_engine.extract_date(text),
            "时间": fallback_engine.extract_time_range(text),
            "活动类型": fallback_engine.extract_activity_type(text)
        }
    
    def process_natural_language(self, text: str) -> Dict[str, Any]:
        try:
            if self.model_type == "local":
                prompt = self._build_prompt(text)
                result = self._call_local_model(prompt)
                if not result or not any(result.values()):
                    result = self._fallback_rule_based(text)
                    logger.info("使用规则回退方案")
                else:
                    logger.info("使用大模型处理结果")
                    
            else:  
                result = self._fallback_rule_based(text)
                logger.info("使用规则模式")
            return self._standardize_result(result)
            
        except Exception as e:
            logger.error(f"处理自然语言失败: {e}")
            return self._fallback_rule_based(text)
    
    def _standardize_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        standardized = {
            "年龄": None,
            "人数": 1,
            "日期": None,
            "时间": None,
            "活动类型": "综合"
        }
        age = raw_result.get("年龄")
        if age and isinstance(age, (int, float)) and 1 <= age <= 100:
            standardized["年龄"] = int(age)
        people = raw_result.get("人数", 1)
        if isinstance(people, (int, float)) and 1 <= people <= self.max_people_count:
            standardized["人数"] = int(people)
        elif isinstance(people, str):
            import re
            num_match = re.search(r'\d+', str(people))
            if num_match:
                num = int(num_match.group())
                standardized["人数"] = min(num, self.max_people_count)
        date_str = raw_result.get("日期")
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                if date_obj < self.current_date:
                    date_obj = date_obj.replace(year=self.current_year + 1)
                elif (date_obj - self.current_date).days > self.max_future_days:
                    date_obj = date_obj.replace(year=self.current_year)
                
                standardized["日期"] = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                pass
        time_str = raw_result.get("时间")
        if time_str:
            time_mapping = {
                "上午": "08:00-12:00",
                "下午": "14:00-18:00",
                "早上": "07:00-10:00",
                "中午": "11:00-14:00",
                "晚上": "19:00-22:00"
            }
            standardized["时间"] = time_mapping.get(time_str, time_str)
        activity = raw_result.get("活动类型", "综合")
        if activity and activity in ["环保", "教育", "社区服务", "医疗", "动物保护"]:
            standardized["活动类型"] = activity
        else:
            text_lower = str(activity).lower()
            for activity_type, keywords in self.activity_mapping.items():
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        standardized["活动类型"] = activity_type
                        break
        
        return standardized
    
    def validate_input(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        questions = []
        warnings = []
        
        if not processed_data["日期"]:
            questions.append("请问您希望参加活动的具体日期是？")
        
        if not processed_data["活动类型"] or processed_data["活动类型"] == "综合":
            questions.append("请问您希望参加什么类型的志愿活动？")
        
        if processed_data["年龄"] and (processed_data["年龄"] < 5 or processed_data["年龄"] > 80):
            warnings.append("年龄范围异常，请确认年龄信息")
        
        return {
            "needs_clarification": len(questions) > 0,
            "questions": questions,
            "warnings": warnings
        }
    
    def generate_database_query(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        query = {
            "activity_type": processed_data["活动类型"] if processed_data["活动类型"] != "综合" else None,
            "date": processed_data["日期"],
            "time_range": processed_data["时间"],
            "participants": processed_data["人数"],
            "age_limit": processed_data["年龄"]
        }
        return {k: v for k, v in query.items() if v is not None}
class HybridNLPEngine:
    """混合引擎，支持规则和大模型切换"""
    
    def __init__(self, use_llm: bool = False, **kwargs):
        self.use_llm = use_llm
        if use_llm:
            self.engine = LLMVolunteerNLPEngine(**kwargs)
        else:
            from volunteer_nlp_system import VolunteerNLPEngine
            self.engine = VolunteerNLPEngine()
    
    def process_natural_language(self, text: str) -> Dict[str, Any]:
        return self.engine.process_natural_language(text)
    
    def validate_input(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.engine.validate_input(processed_data)
    
    def generate_database_query(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.engine.generate_database_query(processed_data)


if __name__ == "__main__":
    engine = LLMVolunteerNLPEngine(model_type="rule")  # 先用规则模式测试
    
    test_cases = [
        "我和我朋友都是16岁，我和他要做一个在4月3号上午的志愿活动，我们想做环保类型的",
        "我想一个人参加明天下午的社区服务活动，我18岁了",
        "我们三个人想在4月3号做一些环保相关的事情，都是大学生",
        "明天我想和朋友一起参加敬老院的志愿活动"
    ]
    
    for test in test_cases:
        result = engine.process_natural_language(test)
        validation = engine.validate_input(result)
        query = engine.generate_database_query(result)
        
        print(f"输入: {test}")
        print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print(f"验证: {validation}")
        print(f"查询: {query}")
        print("-" * 50)