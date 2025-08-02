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
        
        
        self.assertEqual(self.nlp_engine.extract_age("我十八岁"), None) 
        self.assertEqual(self.nlp_engine.extract_age("我十八岁了"), None)
        
       
        self.assertIsNone(self.nlp_engine.extract_age("我想参加活动"))
    
    def test_extract_people_count(self):
        
       
        self.assertEqual(self.nlp_engine.extract_people_count("我们3个人"), 3)
        self.assertEqual(self.nlp_engine.extract_people_count("我一个人"), 1)
        
       
        self.assertEqual(self.nlp_engine.extract_people_count("我和朋友"), 2)
        self.assertEqual(self.nlp_engine.extract_people_count("我和他们"), 3)
        self.assertEqual(self.nlp_engine.extract_people_count("我和我朋友"), 2)
        
      
        self.assertEqual(self.nlp_engine.extract_people_count("我们两个人"), 2)
    
    def test_extract_date(self):

        self.assertEqual(self.nlp_engine.extract_date("4月3日"), "2024-04-03")
        self.assertEqual(self.nlp_engine.extract_date("4月3号"), "2024-04-03")
        self.assertEqual(self.nlp_engine.extract_date("4/3"), "2024-04-03")
        

        from datetime import datetime, timedelta
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        self.assertEqual(self.nlp_engine.extract_date("明天"), tomorrow.strftime('%Y-%m-%d'))
    
    def test_extract_time_range(self):

        self.assertEqual(self.nlp_engine.extract_time_range("8点到12点"), "08:00-12:00")
        self.assertEqual(self.nlp_engine.extract_time_range("上午9点到11点"), "09:00-11:00")
        

        self.assertEqual(self.nlp_engine.extract_time_range("上午"), "08:00-12:00")
        self.assertEqual(self.nlp_engine.extract_time_range("下午"), "14:00-18:00")
    
    def test_extract_activity_type(self):
  
        self.assertEqual(self.nlp_engine.extract_activity_type("环保活动"), "环保")
        self.assertEqual(self.nlp_engine.extract_activity_type("捡垃圾"), "环保")

        self.assertEqual(self.nlp_engine.extract_activity_type("教育活动"), "教育")
        self.assertEqual(self.nlp_engine.extract_activity_type("支教"), "教育")

        self.assertEqual(self.nlp_engine.extract_activity_type("敬老院"), "社区服务")
        self.assertEqual(self.nlp_engine.extract_activity_type("社区活动"), "社区服务")

        self.assertEqual(self.nlp_engine.extract_activity_type("随便什么活动"), "综合")
    
    def test_full_processing(self):
        text = "我和我朋友都是16岁，我和他要做一个在4月3号上午的志愿活动，我们想做环保类型的"
        result = self.nlp_engine.process_natural_language(text)
        
        self.assertEqual(result["年龄"], 16)
        self.assertEqual(result["人数"], 2)
        self.assertEqual(result["日期"], "2024-04-03")
        self.assertEqual(result["时间"], "08:00-12:00")
        self.assertEqual(result["活动类型"], "环保")
    
    def test_database_search(self):
        query = {
            "activity_type": "环保",
            "date": "2024-04-03",
            "time_range": "08:00-12:00",
            "participants": 2,
            "age_limit": 16
        }
        
        results = self.database.search_projects(query)
        self.assertTrue(len(results) > 0)
        
        for project in results:
            self.assertEqual(project["type"], "环保")
            self.assertEqual(project["date"], "2024-04-03")
            self.assertGreaterEqual(project["max_participants"], 2)
    
    def test_edge_cases(self):
        text = "我想参加志愿活动"
        result = self.nlp_engine.process_natural_language(text)
        
        self.assertEqual(result["人数"], 1)  
        self.assertEqual(result["活动类型"], "综合")  

if __name__ == '__main__':
    print("开始运行志愿项目NLP系统测试...")
    unittest.main(verbosity=2)