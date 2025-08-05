# ChatGPT Web Python Flask Version

This is a ChatGPT Web application reimplemented using the Python Flask framework. The project is based on the open source project [ChatGPT-Web](https://github.com/Chanzhaoyu/chatgpt-web), which originally used Node.js as the backend. This project replaces the backend with Python Flask to meet different technical requirements, while preserving the original built static files for the frontend.

## Features

- Complete ChatGPT conversation functionality
- Streaming response output (typewriter effect)
- Support for custom system prompts
- Support for temperature and Top-P parameter adjustment
- API key authentication support
- Multiple model configuration support
- Proxy settings support (HTTPS, SOCKS)

## Tech Stack

- Backend: Python Flask
- Frontend: Static files built from the original project
- API: OpenAI API (supports official API and custom APIs such as Zhipu AI)

## System Requirements

- Python 3.7+
- OpenAI API key or compatible API service

## Installation Steps

### 1. Get the Project Code

```bash
git clone https://github.com/RichardZ217/chatgptweb-second.git
cd chatgptweb-second
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create or edit the `.env` file and set the necessary configurations:

```
# OpenAI API Key
OPENAI_API_KEY=your-api-key-here

# API Base URL, can use custom API services
OPENAI_API_BASE_URL=https://api.openai.com
# Or use other AI service providers, such as Zhipu AI
# OPENAI_API_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# Choose model
OPENAI_API_MODEL=gpt-3.5-turbo

# Timeout setting
TIMEOUT_MS=100000

# Optional: Set a secret key
AUTH_SECRET_KEY=your-secret-key

# Optional: Proxy settings
# HTTPS_PROXY=http://127.0.0.1:7890
# SOCKS_PROXY_HOST=127.0.0.1
# SOCKS_PROXY_PORT=7891
```

## Running the Application

```bash
python run.py
```

The service will start on `http://localhost:3002`.

## API Documentation

### Chat Interface

- **POST /api/chat-process**
  - Function: Process chat requests
  - Request body:
    ```json
    {
      "prompt": "Hello",
      "options": {},
      "systemMessage": "You are a helpful assistant",
      "temperature": 0.7,
      "top_p": 1
    }
    ```
  - Response: Streaming response, each chunk is a JSON object

### Configuration Interface

- **POST /api/config**
  - Function: Get system configuration
  - Response: Returns current configuration information

### Session Interface

- **POST /api/session**
  - Function: Get session information
  - Response: Returns authentication status and current model being used

### Verification Interface

- **POST /api/verify**
  - Function: Verify access key
  - Request body:
    ```json
    {
      "token": "your-secret-key"
    }
    ```
  - Response: Returns verification result

## Frontend-Backend Structure

This project adopts a front-end and back-end separation architecture:

- **Frontend**: Uses the original project's built static files, located in the `static` directory
- **Backend**: API service rewritten with Python Flask, providing the same API interfaces as the original project

The advantages of this design include:
1. Maintains the excellent frontend user experience of the original project
2. Uses Python for the backend, making it easier to integrate with other Python ecosystem tools and libraries
3. Allows for more flexible secondary development and feature extensions

## Project Structure

```
chatgptweb-second/
├── app/                  # Application main directory
│   ├── api/              # API routes
│   ├── core/             # Core configuration
│   ├── services/         # Service layer
│   ├── utils/            # Utility functions
│   ├── middleware/       # Middleware
│   └── __init__.py       # Application initialization
├── static/               # Frontend static files (built from original project)
├── requirements.txt      # Dependency list
├── run.py                # Startup script
├── check_structure.py    # Directory structure check
└── .env                  # Environment variable configuration
```

## Custom Models

This project defaults to using OpenAI's API, but you can also configure it to use other AI service providers compatible with the OpenAI API, such as Zhipu AI. Simply modify the `OPENAI_API_BASE_URL` and `OPENAI_API_MODEL` in the `.env` file.

## Common Issues

1. **Streaming Response Lag**
   - Check if the network connection is stable
   - API response might be slow; try using an API service closer to your geographic location
   - Check if your server resources are sufficient

2. **API Key Authentication Failure**
   - Confirm that the API key is correctly set in the `.env` file
   - Check if the API key is valid
   - For third-party API services, confirm that the API format meets the requirements

3. **Proxy Setting Issues**
   - Ensure the proxy server is running
   - Verify that the proxy URL or IP address and port are correct

4. **Frontend Access Issues**
   - Confirm that static files are correctly placed in the `static` directory
   - Check if Flask is correctly configured for the static file directory

## Differences from the Original Project

- Backend changed from Node.js to Python Flask
- Maintains API interface compatibility to ensure seamless frontend connection
- Optimized some request processing logic to improve response speed
- Simplified deployment process, no longer requiring Node.js environment

## Contribution

Issues and Pull Requests are welcome to improve this project.

## License

MIT

## Acknowledgements

- Thanks to the original [ChatGPT-Web](https://github.com/Chanzhaoyu/chatgpt-web) project for the frontend implementation
- Thanks to OpenAI for providing the API service
- Thanks to all developers who have contributed to this project
