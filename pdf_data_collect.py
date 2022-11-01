"""
This script is run to fetch research papers information from Arxiv and ACL Anthology
The following data fields are fetched for all papers

from: arxiv or  acl_anthology
title: paper title
authors: paper authors
published: publish data
journal_ref: which journal it was published in - not always present
summary: summary of the paper
pdf_url: pdf url of the research paper

"""
from typing import List
import arxiv
from bs4 import BeautifulSoup
import requests
from acl.paper import Paper
import pandas as pd


def parse_arxiv_results(search):
    """
    Function to parse arxiv results

    Args:
        search: search object from arxiv package

    Returns:
        List: list of dictionaries which contain the search query results
    """
    res = []
    for result in search.results():
        res.append(
            {
                "from": "arxiv",
                "title": result.title,
                "authors": ",".join([author.name for author in result.authors]),
                "published": result.published,
                "journal_ref": result.journal_ref,
                "summary": result.summary,
                "pdf_url": result.pdf_url,
            }
        )
    return res


def get_arxiv_by_search_queries(query: str, max_results=15):
    """
    This function uses the passed in query to create a arxiv
    Search object where the results can limited using the max_results
    argument

    Args:
        query (str): query string - this will be used as search string in arxiv
        max_results (int, optional): Max results we want the arxiv API to return. Defaults to 15.

    Returns:
        List[Dict]: Parsed arxiv search results
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )
    return parse_arxiv_results(search)


def get_arxiv_by_search_ids(ids: List[str]):
    """
    This function uses the passed in ids to create a arxiv
    Search object.

    Only the passed in research paper ids will be fetched

    Args:
        ids (List[str]): arxiv research paper ids

    Returns:
        List[Dict]: parsed arxiv results in form of list of dictionaries 
    """
    search = arxiv.Search(id_list=ids)
    return parse_arxiv_results(search)


def get_acl_anthology(url: str, div_id: str):
    """
    This function is used to fetch papers from ACL Anthology using the
    passed in url

    Args:
        url (str): ACL Anthology URL
        div_id (str): Div id in HTML, the papers under this div will be fetched

    Returns:
        List[Dict]: ACL Anthology results in the form of list of dictionaries
    """
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    div_content = soup.find("div", id=div_id)
    div_content_p = div_content.find_all("p")[1:20:2]
    article_url = "https://aclanthology.org/{}"
    article_pdf_url = "{}.pdf"
    res = []
    for paragraph in div_content_p:
        href = (
            paragraph.find_all("span", class_="d-block")[1]
            .find("strong")
            .find("a")["href"]
        )
        final_article_url = article_url.format(href)
        result = Paper.create_from_page(final_article_url)
        article_soup = BeautifulSoup(
            requests.get(final_article_url).text, "html.parser"
        )
        authors = article_soup.find("p", class_="lead").text
        authors = authors.replace("\n", "").replace("\r", "")
        res.append(
            {
                "from": "acl_anthology",
                "title": result.title,
                "authors": authors,
                "published": "{}/{}".format(result.month, result.year),
                "journal_ref": result.venue,
                "summary": result.abstract,
                "pdf_url": article_pdf_url.format(result.acl_url),
            }
        )
    return res


if __name__ == "__main__":

    # Arxiv search queries and specific paper ids
    arxiv_queries = [
        "Transformers Models NLP",
        "Deep Learning Models NLP",
        "BERT Models NLP",
        "Attention NLP",
        "RNN LSTM Models NLP",
        "BERT Models",
        "NLP Datasets",
    ]
    arxiv_ids = ["1706.03762", "1910.01108", "1907.11692"]
    res = []
    for query in arxiv_queries:
        res.extend(get_arxiv_by_search_queries(query))

    res.extend(get_arxiv_by_search_ids(arxiv_ids))

    # ACL Anthology URLS
    acl_anothology_urls_paper_divs = [
        ("https://aclanthology.org/events/acl-2022/", "2022-acl-short"),
        ("https://aclanthology.org/events/emnlp-2021/", "2021-emnlp-main"),
        ("https://aclanthology.org/events/naacl-2022/", "2022-naacl-main"),
    ]
    for url, div_id in acl_anothology_urls_paper_divs:
        res.extend(get_acl_anthology(url, acl_anothology_urls_paper_divs))

    df = pd.DataFrame.from_dict(res)
    df = df.drop_duplicates()
    df.to_csv("ner_task_pdf_links.csv")
