#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from volunteer_nlp_system import VolunteerNLPEngine, VolunteerDatabase

class TestVolunteerNLPSystem(unittest.TestCase):
    
    def setUp(self):
        self.nlp_engine = VolunteerNLPEngine()
        self.database = VolunteerDatabase()
    
    def test_extract_age(self):
        self.assertEqual(self.nlp_engine.extract_age("我今年16岁"), 16)
        self.assertEqual(self.nlp_engine.extract_age("年龄18周岁"), 18)
        self.assertIsNone(self.nlp_engine.extract_age("我想参加活动"))
    
    def test_extract_people_count(self):
        self.assertEqual(self.nlp_engine.extract_people_count("我们3个人"), 3)
        self.assertEqual(self.nlp_engine.extract_people_count("3个人"), 3)
        self.assertEqual(self.nlp_engine.extract_people_count("我一个人"), 1)
        self.assertEqual(self.nlp_engine.extract_people_count("我和朋友"), 2)
        self.assertEqual(self.nlp_engine.extract_people_count("60个人"), 50)
    
    def test_extract_date(self):
        date_result = self.nlp_engine.extract_date("4月3日")
        if date_result:
            self.assertTrue(date_result.endswith("-04-03"))
        from datetime import datetime, timedelta
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        self.assertEqual(self.nlp_engine.extract_date("明天"), tomorrow_str)
    
    def test_extract_time_range(self):
        self.assertEqual(self.nlp_engine.extract_time_range("上午"), "08:00-12:00")
        self.assertEqual(self.nlp_engine.extract_time_range("下午"), "14:00-18:00")
    
    def test_extract_activity_type(self):
        self.assertEqual(self.nlp_engine.extract_activity_type("环保活动"), "环保")
        self.assertEqual(self.nlp_engine.extract_activity_type("教育活动"), "教育")
        self.assertEqual(self.nlp_engine.extract_activity_type("敬老院"), "社区服务")
        self.assertEqual(self.nlp_engine.extract_activity_type("随便什么活动"), "综合")
    
    def test_validation_past_date(self):
        processed_data = {
            "年龄": 16,
            "人数": 2,
            "日期": "2023-01-01",  # 过去日期
            "时间": "09:00-12:00",
            "活动类型": "环保"
        }
        validation = self.nlp_engine.validate_input(processed_data)
        self.assertTrue(validation["needs_clarification"])
    
    def test_validation_future_date(self):
        from datetime import datetime, timedelta
        future_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        processed_data = {
            "年龄": 16,
            "人数": 2,
            "日期": future_date,
            "时间": "09:00-12:00",
            "活动类型": "环保"
        }
        validation = self.nlp_engine.validate_input(processed_data)
        self.assertFalse(validation["needs_clarification"])
    
    def test_validation_missing_info(self):
        processed_data = {
            "年龄": None,
            "人数": 1,
            "日期": None,
            "时间": None,
            "活动类型": "环保"
        }
        validation = self.nlp_engine.validate_input(processed_data)
        self.assertTrue(validation["needs_clarification"])
        self.assertTrue(len(validation["questions"]) > 0)

if __name__ == '__main__':
    print("开始运行志愿项目NLP系统测试...")
    unittest.main(verbosity=2)