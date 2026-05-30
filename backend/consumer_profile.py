import json
import os

class ConsumerProfile:
    """
    消费者人设管理
    """
    
    # 基础人设
    BASE_PROFILE = {
        "age": 28,
        "location": "二线城市",
        "monthly_income": 8000,
        "skincare_frequency": "高频",
        "gender": "女性",
        "personality": "理性消费者，关注性价比，活跃于护肤社区",
        "values": "追求品质生活，爱护肌肤，享受分享"
    }
    
    def __init__(self):
        self.climate_profiles = self._load_climate_profiles()
        self.skin_profiles = self._load_skin_profiles()
    
    def _load_climate_profiles(self):
        """
        加载气候人设配置
        """
        return {
            "干燥": {
                "humidity_level": "低",
                "skin_concern": "皮肤干燥、脱皮、紧绷",
                "product_focus": "保湿、补水、锁水",
                "frequency": "每天多次补水"
            },
            "闷热": {
                "humidity_level": "高",
                "skin_concern": "粉刺、毛孔堵塞、油腻",
                "product_focus": "清爽、控油、深层清洁",
                "frequency": "早晚各一次"
            },
            "多云": {
                "humidity_level": "中",
                "skin_concern": "不稳定、容易敏感",
                "product_focus": "温和、抗敏感、舒适",
                "frequency": "根据皮肤状况调整"
            },
            "多雨": {
                "humidity_level": "很高",
                "skin_concern": "油腻、粘腻、细菌滋生",
                "product_focus": "控油、抗菌、清爽",
                "frequency": "每天清洁"
            },
            "大风": {
                "humidity_level": "低",
                "skin_concern": "干燥、泛红、脱皮",
                "product_focus": "防护、保湿、修复",
                "frequency": "加强保湿"
            },
            "炎热": {
                "humidity_level": "中高",
                "skin_concern": "晒伤、暗沉、出油",
                "product_focus": "防晒、清爽、美白",
                "frequency": "防晒每4小时补涂"
            },
            "干冷": {
                "humidity_level": "低",
                "skin_concern": "极干、泛红、敏感",
                "product_focus": "深层保湿、舒缓、滋润",
                "frequency": "加强保湿和防护"
            }
        }
    
    def _load_skin_profiles(self):
        """
        加载肤质人设配置
        """
        return {
            "干皮": {
                "oil_water_balance": "缺水缺油",
                "texture": "细腻、容易起皮",
                "common_issues": "干燥、紧绷、细纹、敏感",
                "product_preference": "滋润、营养、柔和",
                "budget_allocation": "30%精华、30%面膜、40%其他"
            },
            "油皮": {
                "oil_water_balance": "油多水少",
                "texture": "油腻、毛孔粗大",
                "common_issues": "粉刺、痘痘、毛孔、暗沉",
                "product_preference": "清爽、控油、清洁",
                "budget_allocation": "20%精华、15%面膜、65%其他"
            },
            "混干皮": {
                "oil_water_balance": "T区油、两颊干",
                "texture": "不均匀、难以护理",
                "common_issues": "T区粉刺、两颊干燥、易敏感",
                "product_preference": "平衡、温和、分区护理",
                "budget_allocation": "40%精华、20%面膜、40%其他"
            },
            "混油皮": {
                "oil_water_balance": "整体偏油、两颊稍干",
                "texture": "容易长痘、毛孔明显",
                "common_issues": "痘痘、毛孔、出油、不均匀",
                "product_preference": "轻盈、控油、修护",
                "budget_allocation": "25%精华、15%面膜、60%其他"
            }
        }
    
    def get_profile(self, climate, skin_type):
        """
        获取综合消费者人设
        """
        profile = self.BASE_PROFILE.copy()
        
        # 添加气候信息
        if climate in self.climate_profiles:
            profile['climate_info'] = {
                "climate": climate,
                **self.climate_profiles[climate]
            }
        
        # 添加肤质信息
        if skin_type in self.skin_profiles:
            profile['skin_info'] = {
                "skin_type": skin_type,
                **self.skin_profiles[skin_type]
            }
        
        return profile
    
    def get_prompt_context(self, climate, skin_type):
        """
        生成用于LLM的消费者人设上下文
        """
        profile = self.get_profile(climate, skin_type)
        
        context = f"""
你是一位28岁的女性消费者，住在二线城市，月入8000元。
你是一个高频护肤用户，对护肤品有一定的了解，关注性价比。

当前环境条件：{climate}
你的肤质：{skin_type}

气候特点：{profile['climate_info']['humidity_level']}湿度
皮肤问题：{profile['climate_info']['skin_concern']}
护理重点：{profile['climate_info']['product_focus']}

肤质特点：{profile['skin_info']['texture']}
常见问题：{profile['skin_info']['common_issues']}

根据这些背景信息，以真实消费者的角度回答问题。
回答要真诚、具体、有个人感受，就像在和朋友聊天一样。
"""
        return context
