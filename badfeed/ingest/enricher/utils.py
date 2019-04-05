from typing import List

import newspaper


def convert_html_to_newspaper(html: str) -> newspaper.Article:
    article = newspaper.api.build_article()
    article.set_html(html)
    article.parse()
    return article


def get_sorted_images(article: newspaper.Article) -> List[str]:
    """Arrange images array whereby the article's top image is the first element."""
    images = list(article.images)
    if article.top_image:
        # TODO this _could_ raise a ValueError
        top_image_index = images.index(article.top_image)
        top_image = images.pop(top_image_index)
        images.insert(0, top_image)
    return images
