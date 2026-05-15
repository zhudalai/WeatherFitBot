def detect_language(text: str) -> str:
    """检测文本语言，返回 zh / ja / en

    规则：
    - 包含日文假名（平假名/片假名）→ ja
    - 包含中文字符（CJK）→ 需要进一步区分中日
    - 纯 ASCII → en

    中日区分：检查是否匹配已知的日语城市名（含汉字）
    """
    # 日文假名 → 确定是日语
    for ch in text:
        code = ord(ch)
        # 平假名 3040-309F，片假名 30A0-30FF
        if 0x3040 <= code <= 0x30FF:
            return "ja"

    # 纯 ASCII → 英语
    if all(ord(ch) < 128 for ch in text.strip()):
        return "en"

    # 包含 CJK 汉字 → 检查是否是已知的日语城市名
    has_cjk = any(0x4E00 <= ord(ch) <= 0x9FFF for ch in text)
    if has_cjk:
        # 如果是已知日语城市名 → ja，否则 → zh
        normalized = text.strip().lower()
        if normalized in _JA_CITY_NAMES:
            return "ja"
        return "zh"

    return "en"


# 日语城市名映射（汉字形式 → 英文查询名）
JA_CITY_MAP = {
    "東京": "Tokyo",
    "大阪": "Osaka",
    "京都": "Kyoto",
    "横浜": "Yokohama",
    "名古屋": "Nagoya",
    "札幌": "Sapporo",
    "神戸": "Kobe",
    "福岡": "Fukuoka",
    "広島": "Hiroshima",
    "仙台": "Sendai",
    "北九州": "Kitakyushu",
    "さいたま": "Saitama",
    "千葉": "Chiba",
    "川崎": "Kawasaki",
    "埼玉": "Saitama",
    "静岡": "Shizuoka",
    "堺": "Sakai",
    "新潟": "Niigata",
    "浜松": "Hamamatsu",
    "熊本": "Kumamoto",
    "相模原": "Sagamihara",
    "練馬": "Nerima",
    "江戸川": "Edogawa",
    "足立": "Adachi",
    "葛飾": "Katsushika",
    "墨田": "Sumida",
    "台東": "Taito",
    "荒川": "Arakawa",
    "品川": "Shinagawa",
    "目黒": "Meguro",
    "大田": "Ota",
    "世田谷": "Setagaya",
    "渋谷": "Shibuya",
    "中野": "Nakano",
    "杉並": "Suginami",
    "豊島": "Toshima",
    "北区": "Kita",
    "板橋": "Itabashi",
    "練馬区": "Nerima",
}

# 用于快速查找的小写集合
_JA_CITY_NAMES = set(JA_CITY_MAP.keys())


def resolve_ja_city(text: str) -> str:
    """将日语城市名解析为英文查询名"""
    stripped = text.strip()
    # 直接匹配
    if stripped in JA_CITY_MAP:
        return JA_CITY_MAP[stripped]
    # 去掉"市"后缀再匹配
    if stripped.endswith("市") and stripped[:-1] in JA_CITY_MAP:
        return JA_CITY_MAP[stripped[:-1]]
    # 原样返回
    return stripped


# OpenWeatherMap 语言代码映射
OWM_LANG_MAP = {
    "zh": "zh_cn",
    "en": "en",
    "ja": "ja",
}

# 穿搭 Prompt 语言映射
PROMPT_LANG_MAP = {
    "zh": "中文",
    "en": "English",
    "ja": "日本語",
}
