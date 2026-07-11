# 📬 PubMed Literature Daily Digest

Automated daily literature digest — fetch the latest papers from PubMed, build a formatted HTML email, and push it to your inbox on a schedule.

Powered by the free NCBI Entrez API (no API key required) and googletrans for optional Chinese translation.

---

## 🚀 Quick Start

### 1. Clone or download

```bash
git clone https://github.com/wangjindongwjd/literature_digest.git
cd literature_digest
```

Or download ZIP from GitHub and unzip.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Requires Python 3.8+.


### 3. Configure

Copy the template and fill in your details:

```bash
copy .env.example .env
```

Edit `.env`:

```bash
# --- Email provider: qq / gmail / 163 / outlook ---
EMAIL_PROVIDER=qq

# --- Your email credentials ---
SENDER_EMAIL=your_email@qq.com
SENDER_PASSWORD=your_smtp_auth_code_here
RECEIVER_EMAIL=your_email@qq.com

# --- PubMed ---
PUBMED_QUERY=pollination
TRANSLATE_ENABLED=false
```

That's it — `EMAIL_PROVIDER` auto-fills the correct SMTP server/port for you. Or set them manually:

```bash
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USE_SSL=false
```

### 4.

### 5. Test it

```bash
python main.py
```

### 6.

### 7. Schedule daily runs
---

## 📄 License

MIT — free to use, modify, and share.


