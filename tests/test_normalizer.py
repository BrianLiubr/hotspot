from app.services.parser.normalizer import clean_html_text, normalize_title, strip_title_noise


def test_clean_html_text():
    assert clean_html_text('<a href="#">测试</a>  文本') == '测试 文本'


def test_strip_title_noise():
    assert strip_title_noise('OpenAI 发布新模型 - 新浪财经') == 'OpenAI 发布新模型'


def test_normalize_title():
    assert normalize_title('OpenAI 发布新模型 - 新浪财经') == 'openai发布新模型'
