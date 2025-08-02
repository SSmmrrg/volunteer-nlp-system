#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import jieba
import jieba.posseg as pseg
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VolunteerNLPEngine:
    def __init__(self):
        self.current_year = datetime.now().year
        self.current_date = datetime.now().date()
        self.max_future_days = 365 
        self.max_people_count = 50  
        self.load_dictionaries()
        
    def load_dictionaries(self):
        environmental_words = [
            '环保', '环境保护', '垃圾分类', '植树', '绿化', '清洁', '捡垃圾',
            '保护地球', '绿色', '生态', '可持续发展', '低碳', '节能'
        ]
        time_words = [
            '上午', '下午', '早上', '中午', '傍晚', '晚上', '凌晨',
            '点', '点钟', '小时', '分钟', '半', '整'
        ]
        number_words = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '两': 2, '俩': 2
        }
        for word in environmental_words + time_words:
            jieba.add_word(word)
            
        self.number_map = number_words
        
    def extract_age(self, text: str) -> Optional[int]:
        age_patterns = [
            r'(\d+)岁',
            r'(\d+)周岁',
            r'年龄(\d+)',
            r'(\d+)岁了'
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
        for chinese_num, arabic_num in self.number_map.items():
            if f'{chinese_num}岁' in text or f'{chinese_num}周岁' in text:
                return arabic_num
                
        return None
    
    def extract_people_count(self, text: str) -> int:
        import re
        match = re.search(r'(\d+)人', text)
        if match:
            count = int(match.group(1))
            return min(count, self.max_people_count)
        for chinese_num, arabic_num in self.number_map.items():
            if f'{chinese_num}个人' in text or f'{chinese_num}人' in text:
                return min(arabic_num, self.max_people_count)
        if '我一个人' in text or '我自己' in text:
            return 1
        elif '我和朋友' in text or '我和我朋友' in text:
            return 2
        elif '我和他们' in text:
            return 3
        elif '两个人' in text or '俩人' in text:
            return 2
        elif '三个人' in text or '我们三个' in text:
            return 3
        elif '我和' in text:
            return 2
            
        return 1  
    
    def extract_date(self, text: str) -> Optional[str]:
        date_patterns = [
            r'(\d+)月(\d+)日',
            r'(\d+)月(\d+)号',
            r'(\d+)/(\d+)',
            r'(\d+)\.(\d+)',
            r'(\d+)月(\d+)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                month = int(match.group(1))
                day = int(match.group(2))
                if 1 <= month <= 12 and 1 <= day <= 31:
                    try:
                        target_date = datetime(self.current_year, month, day).date()
                        if target_date < self.current_date:
                            return None 
                        if (target_date - self.current_date).days > self.max_future_days:
                            return None
                        return target_date.strftime('%Y-%m-%d')
                    except ValueError:
                        return None
        
        today = datetime.now()
        if '明天' in text:
            target_date = today + timedelta(days=1)
            return target_date.strftime('%Y-%m-%d')
        elif '后天' in text:
            target_date = today + timedelta(days=2)
            return target_date.strftime('%Y-%m-%d')
        elif '大后天' in text:
            target_date = today + timedelta(days=3)
            return target_date.strftime('%Y-%m-%d')
            
        return None
    
    def extract_time_range(self, text: str) -> Optional[str]:
        time_patterns = [
            r'(\d+)[点时](\d+)?[到至](\d+)[点时](\d+)?',
            r'(上午|下午|早上|中午|晚上)(\d+)[点时]',
            r'(\d+)[点时]到(\d+)[点时]',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) >= 3:
                    start_hour = int(groups[0] if groups[0] else groups[1])
                    end_hour = int(groups[2] if len(groups) > 2 else groups[1])
                    if '下午' in text and start_hour < 12:
                        start_hour += 12
                        end_hour += 12
                    elif '晚上' in text and start_hour < 12:
                        start_hour += 12
                        end_hour += 12
                        
                    return f"{start_hour:02d}:00-{end_hour:02d}:00"

        if '上午' in text:
            return "08:00-12:00"
        elif '下午' in text:
            return "14:00-18:00"
        elif '中午' in text:
            return "11:00-14:00"
        elif '早上' in text:
            return "07:00-10:00"
            
        return None
    
    def extract_activity_type(self, text: str) -> str:
        text_lower = text.lower()

        environmental_keywords = [
            '环保', '环境保护', '垃圾分类', '植树', '绿化', '清洁', '捡垃圾',
            '保护地球', '绿色', '生态', '可持续发展', '低碳', '节能'
        ]

        education_keywords = [
            '教育', '教学', '辅导', '支教', '培训', '学习', '读书', '知识'
        ]

        community_keywords = [
            '社区', '敬老院', '养老院', '孤儿院', '福利', '关爱', '陪伴',
            '帮助', '服务', '志愿', '公益'
        ]

        medical_keywords = [
            '医疗', '医院', '健康', '献血', '义诊', '救助', '护理'
        ]

        for keyword in environmental_keywords:
            if keyword in text_lower:
                return "环保"
                
        for keyword in education_keywords:
            if keyword in text_lower:
                return "教育"
                
        for keyword in community_keywords:
            if keyword in text_lower:
                return "社区服务"
                
        for keyword in medical_keywords:
            if keyword in text_lower:
                return "医疗"
                
        return "综合"
    
    def validate_input(self, processed_data: Dict) -> Dict:
        questions = []
        warnings = []
        if not processed_data["日期"]:
            questions.append("请问您希望参加活动的具体日期是？")
        else:
            try:
                target_date = datetime.strptime(processed_data["日期"], '%Y-%m-%d').date()
                if target_date < self.current_date:
                    warnings.append("您选择的日期已经过去，请选择未来的日期")
                    processed_data["日期"] = None  # 清除无效日期
                    questions.append("请重新选择未来的活动日期")
                elif (target_date - self.current_date).days > self.max_future_days:
                    warnings.append("您选择的日期太远了，建议选择一年内的日期")
                    processed_data["日期"] = None  # 清除无效日期
                    questions.append("请选择一年内的活动日期")
            except:
                warnings.append("日期格式不正确")
                processed_data["日期"] = None  # 清除无效日期
                questions.append("请提供正确的日期格式，如：4月3日")
        if not processed_data["时间"] or processed_data["时间"] == "09:00-17:00":
            questions.append("请问您希望活动的具体时间段是？")
        if processed_data["人数"] == 1:
            pass
        elif processed_data["人数"] > self.max_people_count:
            warnings.append(f"人数过多，已限制为{self.max_people_count}人")
            processed_data["人数"] = self.max_people_count
        elif processed_data["人数"] > 20:
            questions.append(f"您计划{processed_data['人数']}人参加，请确认具体人数")
        if not processed_data["年龄"] or processed_data["年龄"] == "不限":
            questions.append("请问参与者的年龄大概是多少？")
        
        return {
            "questions": questions,
            "warnings": warnings,
            "needs_clarification": len(questions) > 0
        }
    
    def process_natural_language(self, text: str) -> Dict:
        logger.info(f"处理输入: {text}")
        words = pseg.cut(text)
        logger.info(f"分词结果: {list(words)}")
        result = {
            "原始输入": text,
            "年龄": self.extract_age(text),
            "人数": self.extract_people_count(text),
            "日期": self.extract_date(text),
            "时间": self.extract_time_range(text),
            "活动类型": self.extract_activity_type(text),
            "处理时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        validation = self.validate_input(result)
        if not result["年龄"]:
            result["年龄"] = "不限"
            
        if not result["日期"]:
            result["日期"] = datetime.now().strftime("%Y-%m-%d")
            
        if not result["时间"]:
            result["时间"] = "09:00-17:00"
            
        result["验证结果"] = validation
        
        logger.info(f"处理结果: {result}")
        return result
    
    def generate_database_query(self, processed_data: Dict) -> Dict:
        query = {
            "activity_type": processed_data["活动类型"],
            "date": processed_data["日期"],
            "time_range": processed_data["时间"],
            "participants": processed_data["人数"],
            "age_limit": processed_data["年龄"] if processed_data["年龄"] != "不限" else None
        }
        
        return query

class VolunteerDatabase:
    
    def __init__(self):
        self.projects = [
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
            },
            {
                "id": 2,
                "name": "社区植树活动",
                "type": "环保",
                "date": "2024-04-03",
                "time": "09:00-15:00",
                "age_limit": "8-65",
                "max_participants": 30,
                "description": "在社区公园种植树木，美化环境",
                "location": "东湖社区公园"
            },
            {
                "id": 3,
                "name": "敬老院关爱活动",
                "type": "社区服务",
                "date": "2024-04-03",
                "time": "14:00-17:00",
                "age_limit": "16-70",
                "max_participants": 20,
                "description": "陪伴老人，表演节目，聊天谈心",
                "location": "阳光敬老院"
            },
            {
                "id": 4,
                "name": "青少年环保教育",
                "type": "教育",
                "date": "2024-04-03",
                "time": "10:00-16:00",
                "age_limit": "10-50",
                "max_participants": 25,
                "description": "向青少年宣传环保知识，互动游戏",
                "location": "青少年活动中心"
            }
        ]
    
    def search_projects(self, query: Dict) -> List[Dict]:
        results = []
        
        for project in self.projects:
            match = True

            if query["activity_type"] != "综合" and project["type"] != query["activity_type"]:
                match = False

            if project["date"] != query["date"]:
                match = False

            if project["max_participants"] < query["participants"]:
                match = False

            if query["age_limit"]:
                age_limit_parts = project["age_limit"].split('-')
                min_age = int(age_limit_parts[0])
                max_age = int(age_limit_parts[1])
                user_age = query["age_limit"]
                
                if user_age < min_age or user_age > max_age:
                    match = False
            
            if match:
                results.append(project)
                
        return results

def main():

    print("=== 志愿项目自然语言处理系统 ===\n")
 
    nlp_engine = VolunteerNLPEngine()
    database = VolunteerDatabase()
 
    test_cases = [
        "我和我朋友都是16岁，我和他要做一个在4月3号上午的志愿活动，我们想做环保类型的",
        "我想一个人参加明天下午的社区服务活动，我18岁了",
        "我们三个人想在4月3号做一些环保相关的事情，都是大学生",
        "明天我想和朋友一起参加敬老院的志愿活动"
    ]
    
    for test_text in test_cases:
        print(f"输入: {test_text}")

        processed_data = nlp_engine.process_natural_language(test_text)

        query = nlp_engine.generate_database_query(processed_data)
 
        results = database.search_projects(query)

        print("\n处理结果:")
        for key, value in processed_data.items():
            print(f"  {key}: {value}")
            
        print(f"\n数据库查询条件: {query}")
        
        if results:
            print(f"\n找到 {len(results)} 个匹配项目:")
            for project in results:
                print(f"  - {project['name']} ({project['type']})")
                print(f"    时间: {project['date']} {project['time']}")
                print(f"    地点: {project['location']}")
                print(f"    年龄限制: {project['age_limit']}")
                print(f"    人数限制: {project['max_participants']}人")
                print(f"    描述: {project['description']}")
        else:
            print("\n未找到匹配的项目")
            
        print("-" * 50)

if __name__ == "__main__":
    main()