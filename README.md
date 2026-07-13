# 📬 PubMed Literature Daily Digest

Automated daily literature digest from PubMed. Search any keywords, get formatted HTML digests delivered to your inbox.

---

## 🚀 Quick Start (2 minutes)

```bash
git clone https://github.com/wangjindongwjd/literature_digest.git
cd literature_digest
pip install -r requirements.txt
copy .env.example .env
notepad .env   # fill in your email credentials
python main.py
```

---

## ⚙️ Configuration (.env)

```
# Email provider: qq / gmail / 163 / outlook
EMAIL_PROVIDER=qq

# Your credentials (REQUIRED)
SENDER_EMAIL=your_email@qq.com
SENDER_PASSWORD=your_smtp_auth_code
RECEIVER_EMAIL=your_email@qq.com

# Search keyword (PubMed query syntax supported)
PUBMED_QUERY=pollination

# Translation: true = English + Chinese, false = English only
TRANSLATE_ENABLED=false

# Email branding (customize per instance)
BRAND_TITLE=My Daily Digest
BRAND_EMOJI=📬
BRAND_KEYWORD=my keywords
BRAND_EMPTY_MSG=No new papers today.
```

---

## 📧 Multi-Instance Deployment

Want separate digests for different topics? Just copy the directory:

```bash
# Instance 1: pollination
cd literature_digest
notepad .env   # PUBMED_QUERY=pollination

# Instance 2: meta-analysis
mkdir ../literature_digest_meta
xcopy . ..\literature_digest_meta\ /E /I
cd ../literature_digest_meta
notepad .env   # PUBMED_QUERY="meta analysis"
```

Each instance has its own `.env`, keyword, email branding, and scheduled task. They run completely independently.

---

## ⏰ Schedule Daily Runs

### Windows (Task Scheduler)

Run in **Administrator PowerShell**:

```powershell
$pythonPath = (Get-Command python).Source
$action = New-ScheduledTaskAction -Execute $pythonPath `
    -Argument "YOUR\PATH\main.py" `
    -WorkingDirectory "YOUR\PATH"
$trigger = New-ScheduledTaskTrigger -Daily -At 12:00
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName "LiteratureDigest" `
    -Action $action -Trigger $trigger -Principal $principal
```

### macOS / Linux (cron)

```bash
crontab -e
```
Add: `0 12 * * * cd /path/to/project && python main.py`

---

## 🔍 PubMed Search Syntax

Supports full [PubMed query syntax](https://pubmed.ncbi.nlm.nih.gov/help/#search-tags):

| Example | Meaning |
|---------|---------|
| `pollination` | Keyword anywhere in record |
| `"meta-analysis"[Publication Type]` | Only meta-analysis papers |
| `pollination AND bee` | Both terms must appear |
| `cancer AND (immunotherapy OR CAR-T)` | Grouped logic |
| `Smith J[Author] AND 2024[dp]` | Specific author + year |

Change `PUBMED_QUERY` in `.env` and re-run. No code changes needed.

---

## 📩 Email Provider Presets

| Provider | SMTP Server | Port | `EMAIL_PROVIDER` |
|----------|-------------|------|-------------------|
| QQ | smtp.qq.com | 465 | qq |
| Gmail | smtp.gmail.com | 587 | gmail |
| 163 | smtp.163.com | 465 | 163 |
| Outlook | smtp-mail.outlook.com | 587 | outlook |

For Gmail: enable [App Passwords](https://support.google.com/accounts/answer/185833). For QQ: generate [SMTP auth code](https://service.mail.qq.com/detail/0/75) in settings.

---

## 📁 Project Structure

```
literature_digest/
├── main.py              # Pipeline orchestrator
├── config.py            # All settings (reads .env)
├── pubmed_fetcher.py    # PubMed Entrez API client
├── translator.py        # Google Translate (optional)
├── mail_sender.py       # HTML email builder + SMTP
├── requirements.txt     # pip dependencies
├── .env.example         # Configuration template
├── .gitignore           # Excludes .env and logs
└── logs/                # Daily run logs (auto-rotated)
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| No papers found | Broaden query or check logs |
| Email not received | Check spam; verify SMTP auth code |
| Translation broken | Set `TRANSLATE_ENABLED=false` |
| Entrez error | NCBI rate limit; wait and retry |
| Task Scheduler denied | Run PowerShell as Administrator |
