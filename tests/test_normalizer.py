from app.services.parser.normalizer import clean_html_text


def test_clean_html_text():
    assert clean_html_text('<a href="#">测试</a>  文本') == '测试 文本'
