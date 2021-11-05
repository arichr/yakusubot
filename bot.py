"""Inline bot for Telegram."""
import hashlib
import json
import logging

import aiogram
from aiogram.types import (InlineQuery, InlineQueryResultArticle,
                           InputTextMessageContent)
from aiogram.utils.markdown import hbold, hpre
from aiogram.utils.markdown import text as htext

import translate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

with open('.login') as login:
    login_data = json.load(login)
    API_TOKEN = login_data['key']

bot = aiogram.Bot(API_TOKEN)
dp = aiogram.Dispatcher(bot)

welcome = """
[ Translate by Google API ]
This is a bot created by @arisetta.

1. Type in your target language:
@yakusubot Japanese

2. Type in your text to translate:
@yakusubot Japanese Hello, World!
 Hint: You can add a plus to a language's name to show an original text too.
"""


async def icmd_welcome(inline_query: InlineQuery, languages: dict):
    """Inline welcome command.

    Parameters:
        inline_query: Inline query
        languages: Dict of languages
    """
    lang_text = ['List of available languages:']
    for code, name in languages.items():
        if code == 'auto':
            continue

        lang_text.append('{code} -> {name}'.format(
            code=code,
            name=name,
        ))
    languages_item = InlineQueryResultArticle(
        id='languages',
        title='List of available languages',
        input_message_content=InputTextMessageContent('\n'.join(lang_text)),
    )

    welcome_item = InlineQueryResultArticle(
        id='result',
        title=htext(
            'Welcome! Type in a target language e.g. English or en.',
            'You can add a plus to it for showing an original text too.',
        ),
        input_message_content=InputTextMessageContent(welcome),
    )
    await bot.answer_inline_query(
        inline_query.id,
        results=[welcome_item, languages_item],
    )


async def icmd_translate(inline_query: InlineQuery):
    """Inline translation command.

    Parameters:
        inline_query: Inline query
    """
    text = inline_query.query
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    translation = await translate.from_raw(text)
    qitem = InlineQueryResultArticle(
        id=result_id,
        title=translation.title,
        input_message_content=InputTextMessageContent(translation.text),
    )
    await bot.answer_inline_query(
        inline_query.id,
        results=[qitem],
        cache_time=1,
    )


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    """Inline handler.

    Parameters:
        inline_query: InlineQuery
    """
    text = inline_query.query or 'echo'
    try:
        if text == 'echo':
            languages = await translate.func.list_languages()
            await icmd_welcome(inline_query, languages)
        else:
            await icmd_translate(inline_query)
    except aiogram.exceptions.InvalidQueryID:
        logger.warning('Query is too old.')


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: aiogram.types.Message):
    """Support commands /start and /help.

    Parameters:
        message: Message
    """
    await message.reply(
        htext(
            hbold('[ Translate by Google API ]'),
            '\nThis is a bot created by @arisetta.\n',
            '\n1. Type in your target language:',
            hpre('@yakusubot Japanese'),
            '\n2. Type in your text to translate:',
            hpre('@yakusubot Japanese Hello, World!'),
            hbold(htext(
                "\nHint: You can add a plus to a language's name to show",
                'an original text too.',
            )),
        ),
        parse_mode=aiogram.types.ParseMode.HTML,
    )


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
