# ChatGPT Web Python Flask 版本

这是一个使用Python Flask框架重新实现的ChatGPT Web应用程序。该项目是基于原始Node.js版本的ChatGPT Web项目进行移植，保持了相同的API接口和功能，但后端实现从Node.js改为了Python Flask。

## 功能特点

- 完整的ChatGPT对话功能
- 流式响应输出（打字机效果）
- 支持自定义系统提示词
- 支持温度和Top-P参数调整
- 支持API密钥认证
- 支持多种模型配置
- 支持代理设置（HTTPS、SOCKS）

## 技术栈

- 后端：Python Flask
- 前端：保持原有前端不变
- API：OpenAI API（支持官方API和自定义API）

## 系统要求

- Python 3.7+
- OpenAI API密钥

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/RichardZ217/chatgptweb-second.git
cd chatgptweb-second
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建或编辑 `.env` 文件，设置必要的配置：

```
# OpenAI API Key
OPENAI_API_KEY=your-api-key-here

# API基础URL，可以使用自定义API服务
OPENAI_API_BASE_URL=https://api.openai.com
# 或者使用其他AI服务提供商，如智谱AI
# OPENAI_API_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# 选择模型
OPENAI_API_MODEL=gpt-3.5-turbo

# 超时设置
TIMEOUT_MS=100000

# 可选：设置密钥
AUTH_SECRET_KEY=your-secret-key

# 可选：代理设置
# HTTPS_PROXY=http://127.0.0.1:7890
# SOCKS_PROXY_HOST=127.0.0.1
# SOCKS_PROXY_PORT=7891
```

## 运行应用

```bash
python run.py
```

服务将在 `http://localhost:3002` 上启动。

## API说明

### 聊天接口

- **POST /api/chat-process**
  - 功能：处理聊天请求
  - 请求体：
    ```json
    {
      "prompt": "你好",
      "options": {},
      "systemMessage": "你是一个有用的助手",
      "temperature": 0.7,
      "top_p": 1
    }
    ```
  - 响应：流式响应，每个块是一个JSON对象

### 配置接口

- **POST /api/config**
  - 功能：获取系统配置
  - 响应：返回当前配置信息

### 会话接口

- **POST /api/session**
  - 功能：获取会话信息
  - 响应：返回认证状态和当前使用的模型

### 验证接口

- **POST /api/verify**
  - 功能：验证访问密钥
  - 请求体：
    ```json
    {
      "token": "your-secret-key"
    }
    ```
  - 响应：返回验证结果

## 项目结构

```
chatgptweb-second/
├── app/                  # 应用主目录
│   ├── api/              # API路由
│   ├── core/             # 核心配置
│   ├── services/         # 服务层
│   ├── utils/            # 工具函数
│   ├── middleware/       # 中间件
│   └── __init__.py       # 应用初始化
├── static/               # 静态文件
├── requirements.txt      # 依赖列表
├── run.py                # 启动脚本
├── check_structure.py    # 目录结构检查
└── .env                  # 环境变量配置
```

## 自定义模型

本项目默认使用OpenAI的API，但您也可以配置使用其他兼容OpenAI API的AI服务提供商，如智谱AI等。只需修改`.env`文件中的`OPENAI_API_BASE_URL`和`OPENAI_API_MODEL`即可。

## 贡献

欢迎提交问题和Pull Request来改进此项目。

## 许可证

MIT

## 致谢

- 感谢原始ChatGPT Web项目提供的灵感和前端实现
- 感谢OpenAI提供的API服务
