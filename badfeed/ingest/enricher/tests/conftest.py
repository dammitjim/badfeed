import newspaper
import pytest


@pytest.fixture
def newspaper_article():
    article = newspaper.api.build_article()
    article.images = ["image1", "image2"]
    article.top_image = "image2"
    article.text = "Text"
    article.movies = ["movie1", "movie2"]
    article.summary = "Summary"
    return article
