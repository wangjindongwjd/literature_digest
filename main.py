"""Literature Digest - Daily PubMed Literature Digest Pipeline"""
import logging
import os
import sys
import time
from datetime import datetime, timedelta

from config import (
    LOG_DIR,
    LOG_RETENTION_DAYS,
    EMAIL_SUBJECT_TEMPLATE,
    TRANSLATE_ENABLED,
)
from pubmed_fetcher import fetch_daily_papers
from translator import translate_abstracts
from mail_sender import build_html_digest, send_email


def setup_logging() -> logging.Logger:
    """Set up logging to both file and console."""
    os.makedirs(LOG_DIR, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(LOG_DIR, f"digest_{date_str}.log")

    logger = logging.getLogger("literature_digest")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


def clean_old_logs(log_dir: str, retention_days: int = 7) -> None:
    """Delete log files older than retention_days."""
    if not os.path.isdir(log_dir):
        return

    cutoff = datetime.now() - timedelta(days=retention_days)
    for filename in os.listdir(log_dir):
        if filename.startswith("digest_") and filename.endswith(".log"):
            filepath = os.path.join(log_dir, filename)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mtime < cutoff:
                    os.remove(filepath)
            except OSError:
                continue


def main() -> None:
    """Main pipeline for the daily literature digest."""
    logger = setup_logging()
    logger.info("=== Literature Digest Started ===")

    # Clean old logs
    clean_old_logs(LOG_DIR, LOG_RETENTION_DAYS)
    logger.info("Old logs cleaned (retention: %d days)", LOG_RETENTION_DAYS)

    # Fetch papers
    logger.info("Fetching papers from PubMed...")
    papers = fetch_daily_papers()

    if not papers:
        logger.warning("No new papers found. Exiting.")
        return

    logger.info("Fetched %d papers", len(papers))

    # Translate abstracts (if enabled)
    if TRANSLATE_ENABLED:
        logger.info("Translating abstracts...")
        translate_abstracts(papers)
        logger.info("Translation done")
    else:
        logger.info("Translation disabled (TRANSLATE_ENABLED=False)")

    # Build HTML digest
    date_str = datetime.now().strftime("%Y-%m-%d")
    subject = EMAIL_SUBJECT_TEMPLATE.format(date=date_str)

    logger.info("Building HTML digest...")
    html_content = build_html_digest(papers, date_str)
    logger.info("HTML digest built (%d bytes)", len(html_content))

    # Send email with retry
    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        logger.info("Sending email (attempt %d/%d)...", attempt, max_attempts)
        success = send_email(html_content, subject)

        if success:
            logger.info("Email sent successfully: %s", subject)
            break
        else:
            logger.error("Email sending failed (attempt %d)", attempt)
            if attempt < max_attempts:
                logger.info("Retrying in 10 seconds...")
                time.sleep(10)
    else:
        logger.critical("All email attempts failed. Exiting.")
        sys.exit(1)

    logger.info("=== Literature Digest Complete ===")


if __name__ == "__main__":
    main()
