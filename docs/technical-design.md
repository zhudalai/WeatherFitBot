# 天气穿搭助手 - 技术设计文档

## 1. 技术选型

### 1.1 整体架构
采用 **前后端分离** 架构，前端 Web 页面 + 后端 API 服务。

```
┌─────────────┐     HTTP/REST      ┌──────────────────┐
│   前端 Web   │ ◄──────────────► │     后端 API      │
│  (React)     │                   │   (Python/FastAPI)│
└─────────────┘                    └──────┬───────────┘
                                          │
                         ┌────────────────┼────────────────┐
                         ▼                ▼                ▼
                  ┌──────────────┐ ┌───────────┐ ┌──────────────┐
                  │ OpenWeatherMap│ │  Claude   │ │   Redis      │
                  │    API       │ │   API     │ │  (缓存)      │
                  └──────────────┘ └───────────┘ └──────────────┘
```

### 1.2 前端技术栈

| 技术 | 选型 | 理由 |
|------|------|------|
| 框架 | React 18 + TypeScript | 生态成熟，类型安全 |
| UI 组件库 | Tailwind CSS + Headless UI | 快速开发，高度可定制 |
| 状态管理 | React Hooks (useState/useReducer) | MVP 阶段够用，无需 Redux |
| HTTP 客户端 | Axios | 成熟稳定，拦截器支持 |
| 构建工具 | Vite | 快速冷启动，HMR 体验好 |

### 1.3 后端技术栈

| 技术 | 选型 | 理由 |
|------|------|------|
| 语言 | Python 3.11+ | AI/数据生态丰富，开发效率高 |
| 框架 | FastAPI | 异步支持好，自动生成 API 文档 |
| AI SDK | Anthropic SDK (Claude) | 多语言理解能力强，适合任意语言输入 |
| 缓存 | Redis | 天气数据缓存，减少 API 调用 |

### 1.4 第三方服务

| 服务 | 用途 | 选择理由 |
|------|------|----------|
| OpenWeatherMap API | 天气数据 | 全球覆盖，支持任意语言城市名查询，免费额度 60次/分钟，MVP 够用 |
| Claude API (Anthropic) | 穿搭建议生成 | 多语言理解优秀，城市名消歧能力强，输出格式可控 |

---

## 2. 系统架构

### 2.1 后端模块结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py          # 聊天接口
│   │   └── weather.py       # 天气查询接口
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py    # 天气数据服务
│   │   ├── outfit_service.py     # 穿搭建议服务（AI）
│   │   └── city_resolver.py      # 城市名解析服务
│   ├── models/
│   │   ├── __init__.py
│   │   ├── weather.py       # 天气数据模型
│   │   ├── outfit.py        # 穿搭建议模型
│   │   └── chat.py          # 聊天消息模型
│   ├── cache/
│   │   ├── __init__.py
│   │   └── redis_client.py  # Redis 缓存封装
│   └── utils/
│       ├── __init__.py
│       └── prompts.py       # AI Prompt 模板
├── tests/
├── requirements.txt
└── .env.example
```

### 2.2 前端模块结构

```
frontend/
├── src/
│   ├── main.tsx             # 入口
│   ├── App.tsx              # 根组件
│   ├── components/
│   │   ├── ChatWindow.tsx   # 聊天窗口
│   │   ├── MessageBubble.tsx # 消息气泡
│   │   ├── WeatherCard.tsx  # 天气卡片
│   │   ├── OutfitCard.tsx   # 穿搭建议卡片
│   │   ├── ForecastCard.tsx # 未来天气卡片
│   │   ├── InputBar.tsx     # 输入栏
│   │   └── QuickActions.tsx # 快捷操作按钮
│   ├── hooks/
│   │   ├── useChat.ts       # 聊天逻辑 Hook
│   │   └── useWeather.ts    # 天气数据 Hook
│   ├── services/
│   │   └── api.ts           # API 调用封装
│   ├── types/
│   │   └── index.ts         # TypeScript 类型定义
│   └── styles/
│       └── index.css        # 全局样式
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

---

## 3. API 设计

### 3.1 聊天接口

```
POST /api/chat
Content-Type: application/json

Request:
{
  "message": "上海今天天气怎么样？",
  "session_id": "uuid-string"
}

Response:
{
  "reply": "今天上海...",
  "data": {
    "city": "Shanghai",
    "country": "CN",
    "current_weather": {
      "temperature": 25,
      "feels_like": 27,
      "description": "多云",
      "humidity": 65,
      "wind_speed": 3.5,
      "icon": "02d"
    },
    "outfit_advice": {
      "summary": "今天天气温暖舒适，建议穿轻薄透气的衣物。",
      "top": "短袖T恤或衬衫",
      "bottom": "休闲长裤或九分裤",
      "shoes": "运动鞋或休闲鞋",
      "accessories": "太阳镜、防晒霜",
      "tips": "紫外线较强，注意防晒"
    },
    "forecast": [
      {
        "date": "2026-05-16",
        "temp_max": 28,
        "temp_min": 20,
        "description": "晴",
        "icon": "01d",
        "rain_probability": 0.1
      }
    ]
  },
  "quick_actions": [
    {"label": "换个城市", "action": "change_city"},
    {"label": "查看未来一周", "action": "view_forecast"}
  ]
}
```

### 3.2 天气查询接口

```
GET /api/weather/{city_name}

Response:
{
  "city": "Shanghai",
  "country": "CN",
  "current": { ... },
  "forecast": [ ... ]
}
```

### 3.3 错误响应

```json
{
  "error": {
    "code": "CITY_NOT_FOUND",
    "message": "未找到城市 'Xxx'，请检查城市名称",
    "suggestions": ["Xiamen", "Xian"]
  }
}
```

---

## 4. 核心流程设计

### 4.1 主流程

```
用户输入 ──► 城市名解析 ──► 天气API查询 ──► 数据标准化
                                    │
                                    ▼
                              缓存检查(Redis)
                                    │
                          ┌──── 命中 ────┐
                          │              │
                       返回缓存      调用API获取新数据
                                        │
                                        ▼
                                  写入缓存(TTL=30min)
                                        │
                                        ▼
                              AI穿搭建议生成
                                        │
                                        ▼
                                 结果组装返回
```

### 4.2 城市名解析流程

```
用户输入 ──► 语言检测 ──► 城市名标准化
                              │
                    ┌── 明确 ──┼── 歧义 ──┐
                    │         │          │
                 直接查询   返回候选列表   │
                              │          │
                              └──────────┘
                              用户选择后查询
```

### 4.3 AI 穿搭建议生成流程

```
天气数据 ──► Prompt 构建 ──► Claude API 调用 ──► 结果解析
                                                    │
                                          ┌── 成功 ──┼── 失败 ──┐
                                          │         │          │
                                       返回AI建议  规则引擎兜底   │
                                                              │
                                                    ┌─────────┘
                                                    │
                                              返回基础穿搭建议
```

---

## 5. 数据模型

### 5.1 天气数据模型

```python
class CurrentWeather(BaseModel):
    temperature: float          # 当前温度 (℃)
    feels_like: float           # 体感温度 (℃)
    temp_min: float             # 最低温度
    temp_max: float             # 最高温度
    humidity: int               # 湿度 (%)
    pressure: int               # 气压 (hPa)
    wind_speed: float           # 风速 (m/s)
    wind_direction: int         # 风向 (度)
    description: str            # 天气描述
    icon: str                   # 天气图标代码
    visibility: int             # 能见度 (m)
    uv_index: Optional[float]   # 紫外线指数
    rain_probability: float     # 降水概率

class ForecastDay(BaseModel):
    date: str                   # 日期 (YYYY-MM-DD)
    temp_max: float             # 最高温度
    temp_min: float             # 最低温度
    description: str            # 天气描述
    icon: str                   # 天气图标
    humidity: int               # 湿度
    rain_probability: float     # 降水概率
    wind_speed: float           # 风速

class WeatherResponse(BaseModel):
    city: str                   # 城市名
    country: str                # 国家代码
    current: CurrentWeather
    forecast: List[ForecastDay]
```

### 5.2 穿搭建议模型

```python
class OutfitAdvice(BaseModel):
    summary: str                # 总体建议
    top: str                    # 上装推荐
    bottom: str                 # 下装推荐
    shoes: str                  # 鞋履推荐
    accessories: str            # 配件推荐
    tips: str                   # 特殊提醒
```

### 5.3 聊天消息模型

```python
class ChatMessage(BaseModel):
    role: str                   # "user" | "assistant"
    content: str                # 消息内容
    timestamp: datetime
    data: Optional[dict]        # 附加数据（天气卡片等）

class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    last_city: Optional[str]    # 最近查询的城市
    created_at: datetime
    updated_at: datetime
```

---

## 6. 缓存策略

| 数据类型 | 缓存时间 | 说明 |
|----------|----------|------|
| 当前天气 | 15 分钟 | 天气变化较快 |
| 天气预报 | 30 分钟 | 预报数据相对稳定 |
| 城市搜索结果 | 24 小时 | 城市数据几乎不变 |
| 穿搭建议 | 30 分钟 | 相同天气条件下建议一致 |
| 聊天会话 | 2 小时 | 会话内多轮对话 |

---

## 7. 安全设计

### 7.1 API 密钥管理
- 所有 API 密钥存储在环境变量中
- 使用 `.env` 文件本地开发
- 前端不暴露任何 API 密钥

### 7.2 输入验证
- 城市名长度限制：1-100 字符
- 过滤特殊字符，防止注入攻击
- 请求频率限制：每 IP 30 次/分钟

### 7.3 CORS 配置
- 仅允许前端域名访问 API
- 预检请求缓存 1 小时

---

## 8. 部署方案

### MVP 部署
- **前端**: Vercel / Netlify（静态托管，免费）
- **后端**: Railway / Render（免费额度够用）
- **缓存**: Upstash Redis（Serverless，免费额度）

---

## 9. 监控与日志

### 9.1 关键指标
- API 响应时间（P50/P95/P99）
- 天气 API 调用成功率
- AI 生成成功率
- 缓存命中率

### 9.2 日志规范
- 结构化 JSON 日志
- 请求 ID 追踪
- 错误日志包含上下文信息
