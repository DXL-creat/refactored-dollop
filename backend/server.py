from flask import Flask, request, jsonify
from flask_cors import CORS
from consumer_profile import ConsumerProfile
from llm_adapter import LLMAdapter
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# 初始化消费者档案和LLM适配器
consumer = ConsumerProfile()
llm = LLMAdapter()

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/research', methods=['POST'])
def research():
    """
    生成消费者调研回答
    """
    try:
        data = request.get_json()
        
        # 验证必需参数
        if not all(k in data for k in ['question', 'climate', 'skin_type']):
            return jsonify({
                "error": "Missing required fields: question, climate, skin_type"
            }), 400
        
        question = data['question']
        climate = data['climate']
        skin_type = data['skin_type']
        
        # 验证条件参数
        valid_climates = [
            "干燥", "闷热", "多云", "多雨", "大风", "炎热", "干冷"
        ]
        valid_skin_types = [
            "干皮", "油皮", "混干皮", "混油皮"
        ]
        
        if climate not in valid_climates:
            return jsonify({
                "error": f"Invalid climate. Must be one of: {valid_climates}"
            }), 400
        
        if skin_type not in valid_skin_types:
            return jsonify({
                "error": f"Invalid skin type. Must be one of: {valid_skin_types}"
            }), 400
        
        # 获取消费者人设
        profile = consumer.get_profile(climate, skin_type)
        
        # 生成回答
        answer = llm.generate_response(question, profile)
        
        return jsonify({
            "success": True,
            "question": question,
            "climate": climate,
            "skin_type": skin_type,
            "consumer_profile": profile,
            "answer": answer
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/conditions', methods=['GET'])
def get_conditions():
    """
    获取可用的条件选项
    """
    return jsonify({
        "climates": ["干燥", "闷热", "多云", "多雨", "大风", "炎热", "干冷"],
        "skin_types": ["干皮", "油皮", "混干皮", "混油皮"]
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
