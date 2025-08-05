# ChatGPT Web Python Flask 版本

这是一个使用Python Flask框架重新实现的ChatGPT Web应用程序。该项目是基于开源项目 [ChatGPT-Web](https://github.com/Chanzhaoyu/chatgpt-web) 进行改造，原项目使用 Node.js 作为后端，而本项目将后端改为 Python Flask 以满足不同的技术需求，前端则保留了原有的构建后静态文件。

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
- 前端：使用原项目构建的静态文件
- API：OpenAI API（支持官方API和自定义API如智谱AI等）

## 系统要求

- Python 3.7+
- OpenAI API密钥或兼容的API服务

## 安装步骤

### 1. 获取项目代码

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
# OpenAI API密钥
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

## 前后端结构

本项目采用了前后端分离的架构：

- **前端**：使用原始项目打包构建后的静态文件，位于 `static` 目录下
- **后端**：使用 Python Flask 重写的API服务，提供与原始项目相同的API接口

这样设计的优势在于：
1. 保持了原项目优秀的前端交互体验
2. 使用 Python 实现后端，便于集成其他 Python 生态的工具和库
3. 可以更灵活地进行二次开发和功能扩展

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
├── static/               # 前端静态文件（原项目构建输出）
├── requirements.txt      # 依赖列表
├── run.py                # 启动脚本
├── check_structure.py    # 目录结构检查
└── .env                  # 环境变量配置
```

## 自定义模型

本项目默认使用OpenAI的API，但您也可以配置使用其他兼容OpenAI API的AI服务提供商，如智谱AI等。只需修改`.env`文件中的`OPENAI_API_BASE_URL`和`OPENAI_API_MODEL`即可。

## 常见问题

1. **流式响应卡顿**
   - 检查网络连接是否稳定
   - 可能是API响应速度慢，可以尝试使用更接近您地理位置的API服务
   - 检查您的服务器资源是否充足

2. **API密钥验证失败**
   - 确认`.env`文件中的API密钥已正确设置
   - 检查API密钥是否有效
   - 对于第三方API服务，确认API格式是否符合要求

3. **代理设置问题**
   - 确保代理服务器正在运行
   - 验证代理URL或IP地址和端口是否正确

4. **前端无法访问**
   - 确认静态文件是否正确放置在 `static` 目录下
   - 检查 Flask 是否正确配置了静态文件目录

## 与原项目的区别

- 后端从 Node.js 改为 Python Flask
- 保持了API接口的兼容性，确保前端可以无缝对接
- 优化了部分请求处理逻辑，提高响应速度
- 简化了部署流程，不再需要 Node.js 环境

## 贡献

欢迎提交问题和Pull Request来改进此项目。

## 许可证

MIT

## 致谢

- 感谢原始 [ChatGPT-Web](https://github.com/Chanzhaoyu/chatgpt-web) 项目提供的前端实现
- 感谢OpenAI提供的API服务
- 感谢所有为这个项目做出贡献的开发者
