from flask import g

import os
import config
import json

translations_files_cache = {}


def _load_translations_files(folder='translations', skip_cache=False):

    if len(translations_files_cache) > 0 and not skip_cache:
        return translations_files_cache

    translations_path = os.path.join(config.BASEDIR, folder)

    for file in _get_translations_files(translations_path):
        locale = file.split(".")[0]
        with open(os.path.join(translations_path, file), 'r') as f:
            translations_files_cache[locale] = json.load(f)

    return translations_files_cache


def _get_translations_files(path):
    if not os.path.isdir(path):
        raise RuntimeError('Could not access translations folder.')

    return os.listdir(path)


def localise(key, locale=None, silent=False, **kwargs):
    locale = locale or g.locale
    files = _load_translations_files(skip_cache=config.DEBUG)
    locale_file = files.get(locale)

    if not locale_file:
        raise ValueError(f"No translation file found for selected locale '{locale}'.")

    translation = locale_file.get(key)

    if not translation:
        if silent:
            return key
        raise ValueError(f"No key '{key}' found in locale '{locale}'")

    return translation.format(**kwargs)
