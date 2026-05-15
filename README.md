# 🌤️ WeatherFit - 天气穿搭助手

> 基于天气信息的智能聊天穿搭助手。输入任意城市，获取天气信息和 AI 穿搭建议。

## 项目简介

WeatherFit 是一款 Web 聊天机器人应用。用户用**任意语言**输入城市名称，系统通过天气 API 获取实时天气数据，再通过 AI 模型生成个性化穿搭建议，同时展示未来几天的天气趋势。

### 核心特性

- 🌍 **全球覆盖** - 支持任意语言输入任意城市
- 🤖 **AI 穿搭** - 基于天气数据智能生成穿搭建议
- 💬 **对话交互** - 类聊天应用的自然交互体验
- 📅 **天气趋势** - 未来 3-5 天天气预报
- ⚡ **快速响应** - 缓存机制保障秒级响应

## 技术架构

```
前端 (React + TypeScript + Tailwind CSS)
        │
        ▼ HTTP/REST
后端 (Python + FastAPI)
        │
        ├── OpenWeatherMap API (天气数据)
        ├── Claude API (AI 穿搭建议)
        └── Redis (缓存)
```

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- Redis 7+

### 安装步骤

```bash
# 1. 克隆项目
git clone <repo-url>
cd weatherbot

# 2. 启动后端
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 填入 API Keys
uvicorn app.main:app --reload

# 3. 启动前端
cd ../frontend
npm install
cp .env.example .env  # 填入后端地址
npm run dev

# 4. 访问 http://localhost:5173
```

### 需要的 API Keys

| 服务 | 用途 | 免费额度 |
|------|------|----------|
| [OpenWeatherMap](https://openweathermap.org/api) | 天气数据 | 60次/分钟 |
| [Anthropic Claude](https://console.anthropic.com/) | AI 穿搭建议 | $5 免费额度 |

## 文档

| 文档 | 说明 |
|------|------|
| [需求设计](docs/requirements.md) | 功能需求、用户故事、信息架构 |
| [技术设计](docs/technical-design.md) | 系统架构、API 设计、数据模型 |
| [开发规范](docs/development-guide.md) | 代码规范、Git 规范、迭代计划 |

## 迭代路线

- **Phase 1 - MVP**：基础天气查询 + AI 穿搭 + 聊天界面
- **Phase 2 - 增强**：多轮对话 + 城市歧义处理 + 降级方案
- **Phase 3 - 优化**：用户偏好 + 性能优化 + 分享功能

## License

MIT
