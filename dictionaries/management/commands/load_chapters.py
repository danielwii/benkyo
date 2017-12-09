# -*- coding: utf-8 -*-
import re
from os import listdir, path
from os.path import isfile, join

from django.core.management import BaseCommand
from logzero import logger

from benkyo.settings import BASE_DIR
from dictionaries.models import CHARACTERISTIC_CHOICES


class Command(BaseCommand):
    help = "Load all chapters. Ignore existing words."

    def handle(self, *args, **options):

        search_path = path.join(BASE_DIR, 'chapters')

        logger.info('Searching... %s', search_path)

        all_files = [f for f in listdir(search_path) if isfile(join(search_path, f))]
        logger.info('Files: %s', all_files)

        def extract_word(word: str) -> tuple:
            re_search = re.search(r'(?P<kana>.*)（(?P<kanji>.*)）', word)
            if re_search:
                return re_search.groups()
            else:
                return word, None

        def extract_characteristic(string: str = None) -> tuple:
            if string:
                group = re.search(r'〔(.*)〕', string).group(1)
                return list(filter(lambda c_tuple: c_tuple[1] == group, CHARACTERISTIC_CHOICES))[0]
            else:
                return dict(CHARACTERISTIC_CHOICES).popitem()

        for file in all_files:
            logger.info('Try to load file: %s', file)
            with open(path.join(search_path, file), 'r') as f:
                index = 0
                f_lines = f.readlines()
                for line in f_lines:
                    index += 1
                    logger.info('[%s/%s] Handle: %s', index, len(f_lines), line.strip())
                    parts = line.split()
                    logger.info('Parts: %s', parts)

                    kana, kanji = extract_word(parts[0])
                    logger.info('kana is [%s], kanji is [%s]', kana, kanji)

                    if len(parts) is 2:
                        characteristic = extract_characteristic()
                    elif len(parts) is 3:
                        characteristic = extract_characteristic(parts[1])
                    else:
                        logger.warn('~no such mode handler~ %s', parts)
                        raise ValueError('format not recognised: %s' % parts)

                    meaning = parts[-1]

                    logger.info('characteristic is [%s]', characteristic)
                    logger.info('meaning is [%s]', meaning)
                    logger.info('----------------------------------------------------')
