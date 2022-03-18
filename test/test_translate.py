"""Tests for `notebookc` package."""
import translate


async def test_list_languages():
    """Test the output of languages' list."""
    langs = await translate.list_languages()
    japanese = translate.get_language('ja', langs)
    assert japanese.name == 'Japanese'


async def test_translate():
    """Test the connectivity to Google.Translate."""
    langs = await translate.list_languages()
    target_lang = translate.get_language('en', langs)

    resp = await translate.translate(target_lang, 'Тестовая строка')
    assert resp.text == 'Test string'


async def test_from_raw():
    """Test the Telegram queries' parse function."""
    test_input = 'english тестирование'
    resp = await translate.from_raw(test_input)
    assert resp.text == 'testing'
