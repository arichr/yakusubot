"""Main functions for requesting Google.Translate."""
from http import client as status

import aiohttp

from translate.object import Language, Translation

DUO_TRANS_FORMAT = """
Original:
{orig}
~~~ Yakusu Toshiko (@yakusubot) ~~~
Translation:
{trans}
"""


async def list_languages() -> dict:
    """List available languages.

    Returns:
        dict
    """
    url = 'https://translate.google.com/translate_a/l'
    payload = {
        'hl': 'en_US',
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'client': '',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=payload) as request:
            if request.status != status.OK:
                return Translation(
                    title='Sorry, Google API is not available.',
                    text="Can't connect to Google API. Contact @arisetta.",
                )
            return (await request.json())['sl']


def get_language(raw: str, languages: dict) -> Language:
    """Get a language from a raw string.

    Parameters:
        raw: Input string
        languages: Dict of languages

    Returns:
        Language
    """
    if languages.get(raw):
        return Language(raw, languages[raw])
    else:
        for code, name in languages.items():
            if raw == name:
                return Language(code, name)


async def translate(
    target: Language,
    text: str,
    show_original=False,
) -> Translation:
    """Translate text.

    Parameters:
        target: Target language
        text: Your text
        show_original: Show original text?

    Returns:
        Translation
    """
    url = 'https://translation.googleapis.com/language/translate/v2'
    payload = {
        'key': 'AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw',
        'q': text,
        'target': target.code,
        'format': 'text',
        'source': '',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=payload) as request:
            if request.status != status.OK:
                return Translation(
                    title='Sorry, Google API is not available.',
                    text="Can't connect to Google API. Contact @arisetta.",
                )

            translation = (await request.json())['data']
            translation = translation['translations'][0]['translatedText']

            return Translation(
                title='<{lang}> {result}'.format(
                    lang=target.name,
                    result=translation,
                ),
                text=DUO_TRANS_FORMAT.format(
                    orig=text,
                    trans=translation,
                ) if show_original else translation,
            )


async def from_raw(raw_query: str) -> Translation:
    """Parse a raw Telegram query.

    Parameters:
        raw_query: str

    Returns:
        Translation
    """
    try:
        cut_pos = raw_query.index(' ')
        if len(raw_query.split(' ')) < 2:
            raise ValueError('Not enough arguments.')
    except ValueError:
        return Translation(
            title='Write a target language e.g. English or en.',
            text='Missing a target language. Please, specify it next time.',
        )

    target = raw_query[:cut_pos].title()
    text = raw_query[cut_pos+1:]

    show_original = target[-1] == '+'
    if show_original:
        target = target[:-1]

    languages = await list_languages()
    if isinstance(languages, Translation):
        return languages  # An error has occurred

    target = get_language(target, languages)
    if not target:
        return Translation(
            title='Language is unknown. Try again.',
            text='Missing a target language. Please, specify it next time.',
        )

    return await translate(target, text, show_original)
