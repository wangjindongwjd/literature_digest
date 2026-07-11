# ===============================================
# 传粉方向 PubMed 文献日报 - 配置文件
# ===============================================
# 设置: 复制 .env.example 为 .env 并填入你的信息
# 切换邮箱: 只需改 EMAIL_PROVIDER (qq/gmail/163/outlook)

import os
from pathlib import Path

# --- .env 文件加载（必须在读取任何配置之前） ---
_ENV_FILE = Path(__file__).parent / ".env"
if _ENV_FILE.exists():
    with open(_ENV_FILE, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _key, _, _value = _line.partition("=")
            _key, _value = _key.strip(), _value.strip().strip("'").strip('"')
            if _key and _key not in os.environ:
                os.environ[_key] = _value

# ===============================================
# PubMed 检索
# ===============================================
PUBMED_QUERY = os.getenv("PUBMED_QUERY", "pollination")
PUBMED_RETMAX = int(os.getenv("PUBMED_RETMAX", "50"))
PUBMED_DATABASE = "pubmed"

# ===============================================
# 翻译
# ===============================================
TRANSLATE_ENABLED = os.getenv("TRANSLATE_ENABLED", "false").lower() == "true"

# ===============================================
# 日志
# ===============================================
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "7"))

# ===============================================
# 邮件主题
# ===============================================
EMAIL_SUBJECT_TEMPLATE = os.getenv("EMAIL_SUBJECT", "\U0001f4ec 传粉方向文献日报 - {date}")

# ===============================================
# 邮箱 SMTP（支持预设 + 手动）
# ===============================================
_EMAIL_PRESETS = {
    "qq":      {"server": "smtp.qq.com",       "port": 465, "ssl": True},
    "gmail":   {"server": "smtp.gmail.com",    "port": 587, "ssl": False},
    "163":     {"server": "smtp.163.com",      "port": 465, "ssl": True},
    "outlook": {"server": "smtp-mail.outlook.com", "port": 587, "ssl": False},
}

_provider = os.getenv("EMAIL_PROVIDER", "").lower()
if _provider in _EMAIL_PRESETS:
    _preset = _EMAIL_PRESETS[_provider]
    SMTP_SERVER = _preset["server"]
    SMTP_PORT = _preset["port"]
    SMTP_USE_SSL = _preset["ssl"]
else:
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.qq.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "true").lower() == "true"

# ===============================================
# 邮箱账号
# ===============================================
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECEIVER_EMAIL = [e.strip() for e in os.getenv("RECEIVER_EMAIL", os.getenv("SENDER_EMAIL", "")).split(",") if e.strip()]

