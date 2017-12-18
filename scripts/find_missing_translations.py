import os
import json
import re

import config


translations_path = os.path.join(config.BASEDIR, 'translations')
translation_files = {}


def run(verbose=False):
    for filename in os.listdir(translations_path):
        locale = filename.split(".")[0]
        with open(os.path.join(translations_path, filename), 'r') as f:
            translation_files[locale] = json.load(f)

    for dirpath, dirnames, files in os.walk(config.BASEDIR):
        for name in files:
            if name.lower().endswith('.py') or name.lower().endswith('.jinja2'):
                with open(os.path.join(dirpath, name), 'r') as f:
                    if verbose:
                        print(f'{dirpath}/{name}')
                    check_file_for_missing_translations(f, verbose)


def check_file_for_missing_translations(f, verbose=False):
    file_contents = f.read()
    m = re.findall(r"localise\('(.*)'", file_contents)
    for locale, translation_file in translation_files.items():
        for localisation in m:
            if verbose:
                print(f'--> {localisation}')
            if not translation_file.get(localisation):
                print(f'{localisation} not found in file {locale}')
            if verbose:
                print(f'----> Exists.')



if __name__ == '__main__':
    run(verbose=False)





