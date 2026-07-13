"""
PubMed Fetcher Module

Uses Biopython's Entrez API to search PubMed for "pollination" keyword papers
from the past 24 hours and fetch their details.
"""

import time
from typing import Any

from Bio import Entrez
from config import PUBMED_QUERY

# NCBI requires a valid email address for Entrez API access
Entrez.email = "2747245989@qq.com"


def search_pubmed(query: str, retmax: int = 50) -> list[str]:
    """Search PubMed and return a list of PMIDs.

    Parameters
    ----------
    query : str
        Search query string.
    retmax : int, optional
        Maximum number of results to return (default 50).

    Returns
    -------
    list[str]
        List of PubMed IDs (PMIDs) matching the query.
    """
    try:
        handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=retmax,
            reldate=1,
            datetype="pdat",
            sort="relevance",
        )
        record = Entrez.read(handle)
        handle.close()
        return record.get("IdList", [])
    except Exception as e:
        print(f"Error searching PubMed: {e}")
        return []


def fetch_details(pmid_list: list[str]) -> list[dict[str, Any]]:
    """Fetch full details for a list of PMIDs from PubMed.

    Parameters
    ----------
    pmid_list : list[str]
        List of PubMed IDs to fetch.

    Returns
    -------
    list[dict[str, Any]]
        List of dictionaries, each containing:
        - pmid: str
        - title: str
        - authors: list[str] (formatted as "LastName ForeName")
        - journal: str
        - year: str
        - abstract: str
        - doi: str or empty
        - url: str
    """
    if not pmid_list:
        return []

    try:
        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(pmid_list),
            retmode="xml",
        )
        records = Entrez.read(handle)
        handle.close()
    except Exception as e:
        print(f"Error fetching details from PubMed: {e}")
        return []

    results: list[dict[str, Any]] = []
    articles = records.get("PubmedArticle", [])

    for article in articles:
        try:
            medline = article.get("MedlineCitation", {})
            article_data = medline.get("Article", {})

            # PMID
            pmid = str(medline.get("PMID", ""))

            # Title
            title = str(article_data.get("ArticleTitle", ""))

            # Authors
            author_list = article_data.get("AuthorList", [])
            authors: list[str] = []
            for author in author_list:
                last = author.get("LastName", "")
                fore = author.get("ForeName", "")
                if last or fore:
                    authors.append(f"{last} {fore}".strip())

            # Journal
            journal_data = article_data.get("Journal", {})
            journal = str(journal_data.get("Title", ""))

            # Year
            journal_issue = journal_data.get("JournalIssue", {})
            pub_date = journal_issue.get("PubDate", {})
            # PubDate can be a string or a dict with Year/Month/Day keys
            year = (
                str(pub_date.get("Year", ""))
                if isinstance(pub_date, dict)
                else str(pub_date) if pub_date else ""
            )

            # Abstract
            abstract_parts = []
            abstract_elem = article_data.get("Abstract", {})
            abstract_texts = abstract_elem.get("AbstractText", [])
            for at in abstract_texts:
                label = at.attributes.get("Label") if hasattr(at, "attributes") else None
                text = str(at) if at is not None else ""
                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)
            abstract = "\n".join(abstract_parts)

            # DOI
            article_ids = article.get("PubmedData", {}).get("ArticleIdList", [])
            doi = ""
            for aid in article_ids:
                if hasattr(aid, "attributes") and aid.attributes.get("IdType") == "doi":
                    doi = str(aid)
                    break

            # URL
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            results.append(
                {
                    "pmid": pmid,
                    "title": title,
                    "authors": authors,
                    "journal": journal,
                    "year": year,
                    "abstract": abstract,
                    "doi": doi,
                    "url": url,
                }
            )
        except Exception as e:
            print(f"Error parsing article (PMID may be missing): {e}")
            continue

    return results


def fetch_daily_papers() -> list[dict[str, Any]]:
    """Convenience function: search PubMed for 'pollination' papers
    from the past 24 hours and fetch their details.

    A 1-second sleep is inserted between the search and fetch calls
    to comply with NCBI's rate-limiting guidelines.

    Returns
    -------
    list[dict[str, Any]]
        List of article detail dictionaries.
    """
    pmids = search_pubmed(PUBMED_QUERY)
    if not pmids:
        print("No papers found in the past 24 hours.")
        return []

    print(f"Found {len(pmids)} papers. Fetching details...")
    time.sleep(1)  # NCBI rate limit: 1 request per second without API key
    details = fetch_details(pmids)
    print(f"Successfully fetched details for {len(details)} papers.")
    return details


if __name__ == "__main__":
    papers = fetch_daily_papers()
    for i, paper in enumerate(papers, 1):
        print(f"\n--- Paper {i} ---")
        print(f"PMID:   {paper['pmid']}")
        print(f"Title:  {paper['title']}")
        print(f"Author: {', '.join(paper['authors'][:3])}")
        if len(paper['authors']) > 3:
            print(f"        ... and {len(paper['authors']) - 3} more")
        print(f"Journal:{paper['journal']}")
        print(f"Year:   {paper['year']}")
        print(f"DOI:    {paper['doi']}")
        print(f"URL:    {paper['url']}")
        if paper['abstract']:
            print(f"Abstract (first 200 chars):\n  {paper['abstract'][:200]}...")
