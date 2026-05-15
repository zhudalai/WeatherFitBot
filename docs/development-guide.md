# 天气穿搭助手 - 开发规范文档

## 1. 项目结构

```
weatherbot/
├── docs/                    # 项目文档
│   ├── requirements.md      # 需求设计
│   ├── technical-design.md  # 技术设计
│   └── development-guide.md # 开发规范（本文件）
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/             # API 路由
│   │   ├── services/        # 业务逻辑
│   │   ├── models/          # 数据模型
│   │   ├── cache/           # 缓存封装
│   │   └── utils/           # 工具函数
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/      # 组件
│   │   ├── hooks/           # 自定义 Hooks
│   │   ├── services/        # API 调用
│   │   ├── types/           # 类型定义
│   │   └── styles/          # 样式
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── .gitignore
└── README.md
```

---

## 2. 后端开发规范

### 2.1 Python 代码规范

#### 风格
- 遵循 **PEP 8** 规范
- 使用 **Black** 格式化代码（行宽 88）
- 使用 **isort** 排序 import
- 使用 **mypy** 进行类型检查

#### 命名规范
| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `WeatherService` |
| 函数/方法 | snake_case | `get_weather` |
| 常量 | UPPER_SNAKE | `API_BASE_URL` |
| 私有方法 | _leading_underscore | `_parse_response` |
| 模块文件 | snake_case | `weather_service.py` |

#### 类型注解
- 所有函数必须有类型注解
- 使用 `Optional[X]` 表示可空类型
- 使用 Pydantic 模型定义 API 数据

```python
# Good
async def get_weather(city: str) -> WeatherResponse:
    ...

# Bad
async def get_weather(city):
    ...
```

#### 文档字符串
- 模块级 docstring 说明模块用途
- 公共函数/类必须有 docstring
- 使用 Google Style docstring

```python
async def get_weather(city: str) -> WeatherResponse:
    """获取指定城市的天气信息。

    Args:
        city: 城市名称，支持任意语言。

    Returns:
        WeatherResponse: 包含当前天气和预报数据。

    Raises:
        CityNotFoundError: 当城市不存在时。
        APIError: 当天气 API 调用失败时。
    """
```

### 2.2 API 设计规范

#### RESTful 设计
- 使用名词复数表示资源集合：`/api/weather`
- 使用 HTTP 方法表达动作：GET（查询）、POST（创建）
- 路径中不使用动词

#### 响应格式
统一响应结构：
```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

错误响应：
```json
{
  "code": 404,
  "message": "City not found",
  "error": {
    "type": "CITY_NOT_FOUND",
    "suggestions": ["Shanghai", "Shenzhen"]
  }
}
```

#### HTTP 状态码
| 状态码 | 场景 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用（降级） |

### 2.3 错误处理规范

```python
# 自定义异常
class WeatherBotException(Exception):
    """基础异常类"""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

class CityNotFoundError(WeatherBotException):
    def __init__(self, city: str):
        super().__init__(
            message=f"City '{city}' not found",
            code="CITY_NOT_FOUND"
        )
```

全局异常处理：
```python
@app.exception_handler(WeatherBotException)
async def weatherbot_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message}
    )
```

### 2.4 测试规范

#### 测试框架
- **pytest** 作为测试框架
- **pytest-asyncio** 支持异步测试
- **httpx** 用于 API 测试
- **pytest-mock** 用于 mock 外部依赖

#### 测试结构
```python
class TestWeatherService:
    """天气服务测试"""

    @pytest.fixture
    def weather_service(self):
        return WeatherService()

    @pytest.mark.asyncio
    async def test_get_weather_valid_city(self, weather_service):
        """测试有效城市名查询"""
        result = await weather_service.get_weather("Shanghai")
        assert result.city == "Shanghai"
        assert result.current.temperature is not None

    @pytest.mark.asyncio
    async def test_get_weather_invalid_city(self, weather_service):
        """测试无效城市名查询"""
        with pytest.raises(CityNotFoundError):
            await weather_service.get_weather("InvalidCityName123")
```

#### 测试覆盖率目标
- 核心业务逻辑：≥ 90%
- API 路由：≥ 80%

---

## 3. 前端开发规范

### 3.1 TypeScript 规范

#### 类型定义
```typescript
// types/index.ts
interface WeatherData {
  city: string;
  country: string;
  current: CurrentWeather;
  forecast: ForecastDay[];
}

interface CurrentWeather {
  temperature: number;
  feelsLike: number;
  description: string;
  humidity: number;
  windSpeed: number;
  icon: string;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  weatherData?: WeatherData;
  outfitAdvice?: OutfitAdvice;
}
```

#### 命名规范
| 类型 | 规范 | 示例 |
|------|------|------|
| 组件 | PascalCase | `WeatherCard` |
| 函数/方法 | camelCase | `fetchWeather` |
| 常量 | UPPER_SNAKE | `API_BASE_URL` |
| 接口 | PascalCase | `WeatherData` |
| 文件名(组件) | PascalCase | `WeatherCard.tsx` |
| 文件名(其他) | camelCase | `useChat.ts` |

### 3.2 React 组件规范

#### 组件结构
```typescript
interface WeatherCardProps {
  weather: CurrentWeather;
  city: string;
}

const WeatherCard: React.FC<WeatherCardProps> = ({ weather, city }) => {
  return (
    <div className="weather-card">
      {/* 组件内容 */}
    </div>
  );
};

export default WeatherCard;
```

#### 组件设计原则
- 单一职责：每个组件只做一件事
- Props 类型必须明确定义
- 使用函数式组件 + Hooks
- 避免在 JSX 中写复杂逻辑

#### Hooks 规范
```typescript
export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (content: string) => {
    setIsLoading(true);
    try {
      // 发送消息逻辑
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { messages, isLoading, sendMessage };
}
```

### 3.3 样式规范

#### Tailwind CSS 使用
- 优先使用 Tailwind 原子类
- 避免内样式
- 复杂样式提取为组件变体

```typescript
// Good
<div className="flex items-center gap-4 rounded-lg bg-white p-4 shadow-md">

// Bad
<div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
```

#### 响应式设计
- 移动优先设计
- 断点：`sm:640px` `md:768px` `lg:1024px`
- 聊天界面在移动端全屏显示

### 3.4 API 调用规范

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

export async function sendMessage(message: string, sessionId?: string) {
  const response = await api.post('/api/chat', {
    message,
    session_id: sessionId,
  });
  return response.data;
}
```

---

## 4. Git 规范

### 4.1 分支策略

```
main         生产分支
  └── develop  开发分支
        ├── feature/chat-interface
        ├── feature/weather-api
        ├── feature/outfit-ai
        └── fix/weather-cache-ttl
```

### 4.2 Commit 规范

使用 Conventional Commits 格式：

```
<type>(<scope>): <description>
```

类型：
| 类型 | 用途 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具相关 |

示例：
```
feat(chat): 添加多轮对话支持

- 实现会话 ID 管理
- 添加对话历史缓存
- 支持上下文理解
```

---

## 5. 环境配置

### 5.1 环境变量

后端 `.env`：
```env
# API Keys
OPENWEATHER_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Redis
REDIS_URL=redis://localhost:6379

# App
APP_ENV=development
APP_PORT=8000
CORS_ORIGINS=http://localhost:5173

# Cache TTL (seconds)
WEATHER_CACHE_TTL=900
FORECAST_CACHE_TTL=1800
```

前端 `.env`：
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 5.2 本地开发启动

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # 填入 API Keys
uvicorn app.main:app --reload

# 前端
cd frontend
npm install
cp .env.example .env      # 填入后端地址
npm run dev
```

---

## 6. AI Prompt 规范

### 6.1 穿搭建议 Prompt 模板

```python
OUTFIT_PROMPT_TEMPLATE = """
你是一位专业的穿搭顾问。根据以下天气信息，给出实用的穿搭建议。

天气信息：
- 城市：{city}
- 温度：{temperature}°C（体感 {feels_like}°C）
- 天气：{description}
- 湿度：{humidity}%
- 风速：{wind_speed} m/s
- 紫外线指数：{uv_index}

请用 {language} 回复，按以下 JSON 格式输出：
{{
  "summary": "一句话穿搭建议",
  "top": "上装推荐",
  "bottom": "下装推荐",
  "shoes": "鞋履推荐",
  "accessories": "配件推荐",
  "tips": "特殊提醒"
}}

要求：
1. 建议要实用、具体，避免泛泛而谈
2. 考虑温度、风力、降水等因素
3. 配件要具体（如"带折叠伞"而非"注意防雨"）
4. 语言简洁，每项不超过30字
5. 提供通用穿搭建议，不考虑性别差异
"""
```

### 6.2 Prompt 版本管理
- Prompt 模板存放在 `app/utils/prompts.py`
- 重大修改需记录变更日志

---

## 7. 性能优化

### 7.1 后端优化
- 天气数据缓存（Redis），减少 API 调用
- 异步处理：天气查询和 AI 生成并行
- 连接池复用 HTTP 连接
- Gzip 压缩响应

### 7.2 前端优化
- 天气图标使用 SVG Sprite
- 组件懒加载（React.lazy）
- 防抖处理用户输入
- 乐观更新 UI

---

## 8. 迭代计划

### Phase 1: MVP（1-2 周）
- [x] 项目文档
- [ ] 后端：天气 API 集成
- [ ] 后端：AI 穿搭建议
- [ ] 后端：聊天接口
- [ ] 前端：聊天界面
- [ ] 前端：天气卡片组件
- [ ] 前端：穿搭建议卡片
- [ ] 基础部署

### Phase 2: 增强（2-3 周）
- [ ] 多轮对话支持
- [ ] 城市歧义处理
- [ ] 未来天气趋势图
- [ ] 错误降级处理
- [ ] 单元测试覆盖

### Phase 3: 优化（持续）
- [ ] 用户偏好记忆
- [ ] 性能优化
- [ ] 多语言 UI
- [ ] 分享功能
