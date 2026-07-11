"""邮件格式化和发送模块"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "2747245989@qq.com"
SENDER_PASSWORD = "jpdbqzuatsczdgha"
RECEIVER_EMAIL = "2747245989@qq.com"


def build_html_digest(papers: list[dict], date: str) -> str:
    """生成 HTML 格式的文献日报"""
    items_html = ""
    for i, paper in enumerate(papers, 1):
        title = paper["title"]
        authors = ", ".join(paper["authors"][:5])
        if len(paper["authors"]) > 5:
            authors += " et al."
        journal = paper["journal"]
        year = paper["year"]
        pmid = paper["pmid"]
        doi = paper.get("doi", "")
        abstract = paper.get("abstract", "")
        abstract_cn = paper.get("abstract_cn", "")
        url = paper["url"]

        doi_text = f"DOI: {doi}" if doi else ""
        pmid_text = f"PMID: {pmid}" if pmid else ""

        # 中文摘要区域：仅在有翻译内容时显示
        cn_section = ""
        if abstract_cn:
            cn_section = f"""
                    <p style="margin: 0; color: #333; font-size: 13px; line-height: 1.6; border-top: 1px dashed #dee2e6; padding-top: 8px;">
                        <strong>中文摘要:</strong><br>{abstract_cn}
                    </p>"""

        items_html += f"""
        <div style="margin-bottom: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #2c7be5;">
            <h3 style="margin: 0 0 8px 0; color: #1a1a2e;">
                <a href="{url}" style="color: #2c7be5; text-decoration: none;" target="_blank">{i}. {title}</a>
            </h3>
            <p style="margin: 5px 0; color: #495057; font-size: 13px;">
                👤 {authors}
            </p>
            <p style="margin: 5px 0; color: #6c757d; font-size: 13px;">
                📖 <em>{journal}</em> ({year})
            </p>
            <p style="margin: 5px 0; color: #6c757d; font-size: 12px;">
                {pmid_text}{" | " if pmid_text and doi_text else ""}{doi_text}
            </p>
            <details>
                <summary style="color: #2c7be5; cursor: pointer; font-size: 13px; margin-top: 8px;">📄 查看摘要</summary>
                <div style="margin-top: 8px; padding: 10px; background: #fff; border-radius: 5px; border: 1px solid #e9ecef;">
                    <p style="margin: 0 0 8px 0; color: #333; font-size: 13px; line-height: 1.6;">
                        <strong>EN:</strong><br>{abstract}
                    </p>{cn_section}
                </div>
            </details>
            <p style="margin: 8px 0 0 0;">
                <a href="{url}" style="display: inline-block; padding: 4px 12px; background: #2c7be5; color: #fff; text-decoration: none; border-radius: 4px; font-size: 12px;" target="_blank">🔗 查看原文</a>
            </p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background: #fff;">
    <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #2c7be5; margin-bottom: 25px;">
        <h1 style="color: #1a1a2e; margin: 0; font-size: 24px;">🐝 传粉方向文献日报</h1>
        <p style="color: #6c757d; margin: 5px 0 0 0; font-size: 14px;">📅 {date} | 共检索到 <strong>{len(papers)}</strong> 篇新文献</p>
    </div>
    {items_html}
    <div style="text-align: center; padding: 20px; border-top: 1px solid #dee2e6; margin-top: 20px; color: #adb5bd; font-size: 12px;">
        <p>本日报由 Codex 自动化系统每日 12:00 推送</p>
        <p>关键词: pollination | 数据源: PubMed</p>
    </div>
</body>
</html>"""
    return html




def build_empty_digest(date: str) -> str:
    """生成无新文献的通知邮件"""
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background: #fff;">
    <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #2c7be5; margin-bottom: 25px;">
        <h1 style="color: #1a1a2e; margin: 0; font-size: 24px;">🐝 传粉方向文献日报</h1>
        <p style="color: #6c757d; margin: 5px 0 0 0; font-size: 14px;">📅 {date}</p>
    </div>
    <div style="text-align: center; padding: 40px 20px; background: #f8f9fa; border-radius: 8px;">
        <p style="font-size: 18px; color: #495057; margin: 0;">📭 今日暂无新的 pollination 方向文献</p>
        <p style="font-size: 14px; color: #adb5bd; margin: 10px 0 0 0;">请明天再查看</p>
    </div>
    <div style="text-align: center; padding: 20px; border-top: 1px solid #dee2e6; margin-top: 20px; color: #adb5bd; font-size: 12px;">
        <p>本日报由 Codex 自动化系统每日 12:00 推送</p>
        <p>关键词: pollination | 数据源: PubMed</p>
    </div>
</body>
</html>"""
    return html


def send_email(html_content: str, subject: str) -> bool:
    """Send email via SMTP (SSL or STARTTLS based on SMTP_USE_SSL config)."""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject

        part = MIMEText(html_content, "html", "utf-8")
        msg.attach(part)

        if SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False


