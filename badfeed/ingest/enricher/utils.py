import newspaper


def convert_html_to_newspaper(html: str) -> newspaper.Article:
    article = newspaper.api.build_article()
    article.set_html(html)
    article.parse()
    return article
