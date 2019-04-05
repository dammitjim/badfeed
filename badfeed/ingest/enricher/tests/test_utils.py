import newspaper

from badfeed.ingest.enricher import utils


def test_convert_html_to_newspaper():
    """Should convert the given HTML into a newspaper article object."""
    result = utils.convert_html_to_newspaper(
        "<html><head></head><body><article><p>Hello</p></article>"
    )
    assert isinstance(result, newspaper.Article)


def test_get_sorted_images(newspaper_article):
    """Should sort the top image to the front."""
    newspaper_article.images = ["image1", "image2", "image3"]
    newspaper_article.top_image = "image2"
    assert utils.get_sorted_images(newspaper_article) == ["image2", "image1", "image3"]
