"""Google.Translate module."""
from translate.func import from_raw, translate, list_languages, get_language
from translate.object import Translation

__all__ = [
    'object',
    'func',
    'Translation',
    'from_raw',
]
