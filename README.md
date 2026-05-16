---
title: WeatherFit
emoji: 🌤️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# WeatherFit 🌤️👗

天气穿搭助手 — 输入城市名称，获取实时天气和 AI 穿搭建议。

## 功能

- 🌍 支持中文、英文、日文输入
- 🌡️ 实时天气查询
- 👗 AI 穿搭建议
- 📅 5日天气预报

## API Keys

运行需要以下环境变量：

- `OPENWEATHER_API_KEY` — [OpenWeatherMap](https://openweathermap.org/api) 免费申请
- `OPENROUTER_API_KEY` — [OpenRouter](https://openrouter.ai/) 注册获取

可选：

- `REDIS_URL` — 不设置则自动使用内存缓存

Demo已部署，访问https://weather-fit-bot.vercel.app/
