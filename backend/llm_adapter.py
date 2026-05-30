import openai
import os
from dotenv import load_dotenv

load_dotenv()

class LLMAdapter:
    """
    LLM适配器 - 处理与语言模型的交互
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        openai.api_key = self.api_key
        self.model = "gpt-3.5-turbo"
    
    def generate_response(self, question, profile):
        """
        生成消费者回答
        
        Args:
            question: 调研问题
            profile: 消费者人设
        
        Returns:
            str: AI模拟的消费者回答
        """
        try:
            # 构建系统提示
            system_prompt = self._build_system_prompt(profile)
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # 提取回答
            answer = response.choices[0].message.content.strip()
            return answer
            
        except openai.error.APIError as e:
            return f"API错误: {str(e)}"
        except Exception as e:
            return f"生成回答时出错: {str(e)}"
    
    def _build_system_prompt(self, profile):
        """
        构建系统提示词
        """
        climate_info = profile.get('climate_info', {})
        skin_info = profile.get('skin_info', {})
        
        prompt = f"""
你是一位28岁的女性消费者，住在二线城市，月入8000元。
你是一个高频护肤用户，对护肤品有一定的了解，关注性价比，活跃于小红书等护肤社区。

【当前环境】
气候：{climate_info.get('climate', 'N/A')}
湿度：{climate_info.get('humidity_level', 'N/A')}
皮肤困扰：{climate_info.get('skin_concern', 'N/A')}
护理重点：{climate_info.get('product_focus', 'N/A')}

【你的肤质】
肤质类型：{skin_info.get('skin_type', 'N/A')}
肌肤特征：{skin_info.get('texture', 'N/A')}
常见问题：{skin_info.get('common_issues', 'N/A')}
产品偏好：{skin_info.get('product_preference', 'N/A')}

【回答要求】
1. 从真实消费者的角度回答，不要显得太官方
2. 体现你的个人经验和感受
3. 如果涉及护肤建议，要基于你的肤质和气候条件
4. 可以提到你用过的产品品牌（常见的中端品牌）
5. 回答要具体、有说服力，就像在和朋友聊天
"""
        
        return prompt
