from typing import Optional


class CityResolver:
    """城市名解析服务"""

    # 常见城市别名映射
    ALIASES = {
        "beijing": "Beijing",
        "shanghai": "Shanghai",
        "guangzhou": "Guangzhou",
        "shenzhen": "Shenzhen",
        "hangzhou": "Hangzhou",
        "chengdu": "Chengdu",
        "wuhan": "Wuhan",
        "xian": "Xi'an",
        "nanjing": "Nanjing",
        "chongqing": "Chongqing",
        "北京": "Beijing",
        "上海": "Shanghai",
        "广州": "Guangzhou",
        "深圳": "Shenzhen",
        "杭州": "Hangzhou",
        "成都": "Chengdu",
        "武汉": "Wuhan",
        "西安": "Xi'an",
        "南京": "Nanjing",
        "重庆": "Chongqing",
        "东京": "Tokyo",
        "大阪": "Osaka",
        "首尔": "Seoul",
        "新加坡": "Singapore",
        "曼谷": "Bangkok",
        "伦敦": "London",
        "巴黎": "Paris",
        "纽约": "New York",
        "洛杉矶": "Los Angeles",
        "悉尼": "Sydney",
    }

    @classmethod
    def resolve(cls, city_input: str) -> Optional[str]:
        """解析城市名，返回标准化的城市名"""
        city = city_input.strip()
        lower = city.lower()

        # 直接匹配别名
        if lower in cls.ALIASES:
            return cls.ALIASES[lower]

        # 返回原始输入（让 OpenWeatherMap 去匹配）
        return city
