# WeatherFit 部署指南

## 架构

```
用户 → Vercel (前端 React) → Render (后端 FastAPI) → OpenWeatherMap + OpenRouter
                                    ↓
                              Upstash Redis (缓存)
```

## 前置准备

1. **GitHub 仓库** — 将代码推送到 GitHub
2. **OpenWeatherMap API Key** — 在 https://openweathermap.org/api 免费注册获取
3. **OpenRouter API Key** — 在 https://openrouter.ai 注册获取（有免费额度）
4. **Upstash Redis** — 在 https://upstash.com 免费创建 Redis 数据库，获取 `REDIS_URL`

---

## 第一步：部署后端到 Render

### 1.1 创建 Web Service

1. 访问 https://dashboard.render.com → **New +** → **Web Service**
2. 连接你的 GitHub 仓库
3. 配置：
   - **Name**: `weatherfit-api`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

### 1.2 配置环境变量

在 Render Dashboard → Environment 添加：

| 变量 | 值 |
|------|-----|
| `OPENWEATHER_API_KEY` | 你的 OpenWeatherMap Key |
| `OPENROUTER_API_KEY` | 你的 OpenRouter Key |
| `OPENROUTER_MODEL` | `anthropic/claude-sonnet-4` |
| `REDIS_URL` | 你的 Upstash Redis URL |
| `APP_ENV` | `production` |
| `CORS_ORIGINS` | `https://your-project.vercel.app`（部署 Vercel 后填入） |

### 1.3 记录后端 URL

部署成功后，记录 Render 分配的 URL，格式如：
```
https://weatherfit-api.onrender.com
```

> ⚠️ **注意**：Render 免费版在 15 分钟无请求后会冷启动，首次访问可能需要等待 30-60 秒。

---

## 第二步：部署前端到 Vercel

### 2.1 导入项目

1. 访问 https://vercel.com/dashboard → **Add New** → **Project**
2. 导入你的 GitHub 仓库
3. 配置：
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 2.2 配置环境变量

在 Vercel Dashboard → Settings → Environment Variables 添加：

| 变量 | 值 |
|------|-----|
| `VITE_API_BASE_URL` | `https://weatherfit-api.onrender.com`（你的 Render URL） |

### 2.3 部署

点击 **Deploy**，等待构建完成。

### 2.4 记录前端 URL

部署成功后会获得 URL，格式如：
```
https://weatherfit-xxxxx.vercel.app
```

---

## 第三步：更新后端 CORS

回到 Render Dashboard，将 `CORS_ORIGINS` 更新为你的 Vercel 实际域名：

```
CORS_ORIGINS=https://weatherfit-xxxxx.vercel.app
```

Render 会自动重启服务。

---

## 第四步：验证部署

1. 访问你的 Vercel 前端 URL
2. 在输入框中输入城市名（如 `Tokyo`、`北京`、`東京`）
3. 应该能看到天气信息和穿搭建议

---

## 常见问题

### 前端显示网络错误

- 检查 Vercel 上 `VITE_API_BASE_URL` 是否配置正确
- 确认 Render 服务正在运行
- 检查浏览器控制台的具体错误信息

### CORS 错误

- 确认 Render 上的 `CORS_ORIGINS` 包含你的完整 Vercel 域名（含 `https://`）
- 确保没有多余的斜杠或空格

### Render 服务休眠

- 免费版 Render 会在 15 分钟无活动后休眠
- 首次唤醒需要 30-60 秒，属正常现象
- 可以用 https://cron-job.org 定时 ping 你的 Render URL 来保持活跃

### OpenRouter 额度不足

- 检查 OpenRouter 账户余额（https://openrouter.ai/keys）
- 可以切换到其他免费模型如 `google/gemini-2.0-flash-001`
