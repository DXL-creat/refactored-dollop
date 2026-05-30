# 迷你消费者调研模拟平台

一个基于AI的消费者调研模拟工具，通过设定消费者人设和条件参数，快速生成真实消费者的调研反馈。

## 功能特性

### 1. 消费者人设
- **基础设定**：28岁二线城市女性
- **经济能力**：月入8000元
- **消费习惯**：高频护肤产品使用者
- **品味偏好**：注重性价比、线上社区影响力强

### 2. 调研功能
- 输入开放式调研问题
- AI模拟该消费者给出真实调研回答
- 支持多轮对话

### 3. 条件筛选

#### 气候维度（选一个）
- 干燥
- 闷热
- 多云
- 多雨
- 大风
- 炎热
- 干冷

#### 肤质维度（选一个）
- 干皮
- 油皮
- 混干皮
- 混油皮

## 项目结构

```
.
├── frontend/                 # 前端应用
│   ├── index.html           # 主页面
│   ├── styles.css           # 样式
│   └── app.js               # 前端逻辑
├── backend/                 # 后端服务
│   ├── server.py            # 主服务器
│   ├── consumer_profile.py   # 消费者人设模块
│   ├── llm_adapter.py        # LLM适配器
│   └── requirements.txt      # Python依赖
├── data/                    # 数据配置
│   ├── climate_profiles.json # 气候人设数据
│   └── skin_profiles.json    # 肤质人设数据
└── README.md
```

## 快速开始

### 前置要求
- Python 3.8+
- Node.js 14+
- OpenAI API Key 或其他LLM服务

### 安装

```bash
# 安装后端依赖
cd backend
pip install -r requirements.txt

# 启动服务
python server.py
```

### 使用

1. 打开浏览器访问 `http://localhost:5000`
2. 选择气候条件和肤质
3. 输入调研问题
4. 点击"获取消费者回答"按钮
5. 查看AI模拟的消费者反馈

## API接口

### POST /api/research

生成消费者调研回答

**请求体**：
```json
{
  "question": "你对XXX护肤产品的看法",
  "climate": "干燥",
  "skin_type": "干皮"
}
```

**响应**：
```json
{
  "answer": "AI模拟的消费者回答...",
  "confidence": 0.85
}
```

## 技术栈

- **前端**：HTML5 + CSS3 + Vanilla JavaScript
- **后端**：Python Flask
- **LLM**：OpenAI GPT / 其他大模型
- **数据存储**：JSON配置文件

## 配置说明

### 环境变量

创建 `.env` 文件在backend目录：

```
OPENAI_API_KEY=your-api-key-here
FLASK_ENV=development
PORT=5000
```

## 扩展计划

- [ ] 支持更多消费者人设
- [ ] 多语言支持
- [ ] 调研数据导出
- [ ] 消费者画像库
- [ ] A/B测试模块

## 许可证

MIT
