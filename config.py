import os

class Config:
    USE_LLM = os.getenv('USE_LLM', 'true').lower() == 'true'
    LLM_MODEL_ENDPOINT = os.getenv('LLM_MODEL_ENDPOINT', 'http://localhost:8000/v1/chat/completions')
    LLM_MODEL_TYPE = os.getenv('LLM_MODEL_TYPE', 'qwen-6b-chat')
    LLM_TIMEOUT = int(os.getenv('LLM_TIMEOUT', '30'))
    FALLBACK_TO_RULES = os.getenv('FALLBACK_TO_RULES', 'true').lower() == 'true'
    SUPPORTED_MODELS = {
        'qwen-6b-chat': {
            'name': 'Qwen-6B-Chat',
            'description': '阿里开源中文对话模型',
            'size': '6B参数',
            'url': 'https://huggingface.co/Qwen/Qwen-6B-Chat'
        },
    }

    LLM_MAX_RESPONSE_TIME = 5.0  
    LLM_MAX_CONCURRENT = 10
    
    @classmethod
    def get_model_info(cls, model_name):
        return cls.SUPPORTED_MODELS.get(model_name, {})
    
    @classmethod
    def validate_config(cls):
        errors = []
        
        if cls.USE_LLM:
            if not cls.LLM_MODEL_ENDPOINT.startswith(('http://', 'https://')):
                errors.append("LLM_MODEL_ENDPOINT必须是有效的URL")
            
            if cls.LLM_TIMEOUT < 1 or cls.LLM_TIMEOUT > 300:
                errors.append("LLM_TIMEOUT必须在1-300秒之间")
        
        return errors
    
    @classmethod
    def print_config(cls):
        print("当前系统配置:")
        print(f"  USE_LLM: {cls.USE_LLM}")
        print(f"  LLM_MODEL_ENDPOINT: {cls.LLM_MODEL_ENDPOINT}")
        print(f"  LLM_MODEL_TYPE: {cls.LLM_MODEL_TYPE}")
        print(f"  FALLBACK_TO_RULES: {cls.FALLBACK_TO_RULES}")
        print(f"  LLM_TIMEOUT: {cls.LLM_TIMEOUT}秒")