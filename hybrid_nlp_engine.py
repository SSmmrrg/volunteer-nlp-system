#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging
from typing import Dict
from datetime import datetime
from llm_nlp_engine import LLMVolunteerNLPEngine
from volunteer_nlp_system import VolunteerNLPEngine

logger = logging.getLogger(__name__)

class HybridNLPEngine:
    def __init__(self):
        self.use_llm = os.getenv('USE_LLM', 'false').lower() == 'true'
        self.llm_engine = None
        self.rule_engine = None
        self._initialize_engines()
    
    def _initialize_engines(self):
        try:
            if self.use_llm:
                self.llm_engine = LLMVolunteerNLPEngine(model_type="local")
                logger.info("已启用LLM引擎")
            else:
                logger.info("使用规则引擎")
            
            self.rule_engine = VolunteerNLPEngine()
            
        except Exception as e:
            logger.warning(f"初始化LLM引擎失败: {e}，使用规则引擎")
            self.use_llm = False
    
    def process_natural_language(self, text: str) -> Dict:
        try:
            if self.use_llm and self.llm_engine:
                result = self.llm_engine.process_natural_language(text)
                result["引擎类型"] = "LLM"
                result["原始输入"] = text
                result["处理时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                result = self.rule_engine.process_natural_language(text)
                result["引擎类型"] = "规则"
            
            return result
            
        except Exception as e:
            logger.error(f"处理失败: {e}")
            return self.rule_engine.process_natural_language(text)
    
    def generate_database_query(self, processed_data: Dict) -> Dict:
        if self.use_llm and self.llm_engine:
            return self.llm_engine.generate_database_query(processed_data)
        else:
            return self.rule_engine.generate_database_query(processed_data)
    
    def get_engine_info(self) -> Dict:
        return {
            "当前引擎": "LLM" if self.use_llm else "规则",
            "LLM可用": self.llm_engine is not None,
            "规则引擎可用": self.rule_engine is not None
        }