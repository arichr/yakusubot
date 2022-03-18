"""Dataclasses for the translator."""
from dataclasses import dataclass


@dataclass
class Translation(object):
    """Translation object."""

    title: str = ''
    text: str = ''


@dataclass
class Language(object):
    """Language object."""

    code: str = ''
    name: str = ''
