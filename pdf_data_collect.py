from typing import List
import arxiv
from bs4 import BeautifulSoup
import requests
from acl.paper import Paper
import pandas as pd


def parse_arxiv_results(search):
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
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )
    return parse_arxiv_results(search)


def get_arxiv_by_search_ids(ids: List[str]):
    search = arxiv.Search(id_list=ids)
    return parse_arxiv_results(search)


def get_acl_anthology(url: str, div_id: str):
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
