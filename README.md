# 📬 PubMed Literature Daily Digest

Automated daily literature digest — fetch the latest papers from PubMed, build a formatted HTML email, and push it to your inbox on a schedule.

Powered by the free NCBI Entrez API (no API key required) and googletrans for optional Chinese translation.

---

## 🚀 Quick Start

### 1. Clone or download

```bash
git clone https://github.com/wangjindongwjd/wangjind.git
cd wangjind/literature_digest
```

Or download ZIP from GitHub and unzip.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Requires Python 3.8+.

### 3. Configure

Edit `config.py` — everything you need to change is here:

```python
# --- PubMed Search ---
PUBMED_QUERY = "pollination"           # 🔍 Your search keywords
PUBMED_RETMAX = 50                     # Max papers returned

# --- Email (SMTP) ---
SMTP_SERVER = "smtp.qq.com"            # SMTP server address
SMTP_PORT = 465                        # SMTP port (SSL)
SENDER_EMAIL = "your_email@qq.com"     # Your sender email
SENDER_PASSWORD = "your_auth_code"     # SMTP auth code (NOT your password!)
RECEIVER_EMAIL = "your_email@qq.com"   # Where to receive digests

# --- Translation ---
TRANSLATE_ENABLED = False              # True = English + Chinese, False = English only

# --- Logs ---
LOG_DIR = "logs"
LOG_RETENTION_DAYS = 7                 # Auto-delete logs older than this
```

### 4. Test it

```bash
python main.py
```

If everything works, you will receive a test digest email. Check the terminal output and `logs/` for details.

### 5. Schedule daily runs

**Windows (Task Scheduler):**
Paste the following in an **Administrator PowerShell**:

```powershell
$pythonPath = (Get-Command python).Source
$action = New-ScheduledTaskAction -Execute $pythonPath `
    -Argument "YOUR\PATH\literature_digest\main.py" `
    -WorkingDirectory "YOUR\PATH\literature_digest"
$trigger = New-ScheduledTaskTrigger -Daily -At 12:00
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName "LiteratureDailyDigest" `
    -Action $action -Trigger $trigger -Principal $principal `
    -Description "Daily PubMed literature digest email"
```

Replace `YOUR\PATH\` with the actual directory. Change `-At 12:00` to your preferred time.

**macOS / Linux (cron):**

```bash
crontab -e
```

Add:
```
0 12 * * * cd /path/to/literature_digest && python main.py
```

---

## 🔧 Customization

### Change keywords

Edit `PUBMED_QUERY` in `config.py`. Supports full PubMed query syntax:

```python
PUBMED_QUERY = "pollination AND (bee OR butterfly OR hoverfly)"
PUBMED_QUERY = "(\"climate change\" OR warming) AND biodiversity"
PUBMED_QUERY = "cancer immunotherapy[Title/Abstract]"
```

See [PubMed Search Field Tags](https://pubmed.ncbi.nlm.nih.gov/help/#search-tags) for all options.

### Change time range

By default, the script fetches papers from the last 24 hours (`reldate=1` in `pubmed_fetcher.py`). To change:

```python
# In pubmed_fetcher.py, search_pubmed():
reldate=7    # Last 7 days
reldate=30   # Last 30 days
```

### Use a different email provider

| Provider | SMTP Server | Port | SSL |
|----------|-------------|------|-----|
| QQ | smtp.qq.com | 465 | Yes |
| Gmail | smtp.gmail.com | 587 | STARTTLS |
| 163 | smtp.163.com | 465 | Yes |
| Outlook | smtp-mail.outlook.com | 587 | STARTTLS |

For non-SSL providers (Gmail, Outlook), also change `SMTP_USE_SSL = False` — the script will use STARTTLS instead.

### Add more databases

The project is modular. To add a new source (e.g., arXiv, CrossRef):

1. Create `arxiv_fetcher.py` (or `crossref_fetcher.py`) following the same interface:

```python
def fetch_daily_papers() -> list[dict]:
    """Return list of dicts with keys: pmid, title, authors, journal, year, abstract, doi, url"""
    pass
```

2. In `main.py`, import it and merge papers:

```python
from pubmed_fetcher import fetch_daily_papers
from arxiv_fetcher import fetch_daily_papers as fetch_arxiv_papers

papers = fetch_daily_papers() + fetch_arxiv_papers()
```

---

## 📁 Project Structure

```
literature_digest/
├── main.py              # Entry point -- orchestrates the pipeline
├── config.py            # All configuration in one place
├── pubmed_fetcher.py    # PubMed search & detail fetching (NCBI Entrez)
├── translator.py        # Google Translate wrapper (English -> Chinese)
├── mail_sender.py       # HTML email builder & SMTP sender
├── requirements.txt     # Python dependencies
└── logs/                # Daily run logs (auto-rotated)
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| "No papers found" | Broaden `PUBMED_QUERY` or increase `reldate` in `pubmed_fetcher.py` |
| Email not received | Check spam folder; verify SMTP auth code in `config.py`; check `logs/` for errors |
| Translation errors | Set `TRANSLATE_ENABLED = False`; googletrans may have rate limits |
| "Entrez read error" | NCBI rate limit — wait a few minutes; reduce `PUBMED_RETMAX` |
| Task Scheduler "Access Denied" | Run PowerShell as Administrator |

---

## 📄 License

MIT — free to use, modify, and share.
