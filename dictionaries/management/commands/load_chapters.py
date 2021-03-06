# -*- coding: utf-8 -*-
import json
import re
from os import listdir, path
from os.path import isfile, join

from django.core.management import BaseCommand
from logzero import logger

from benkyo.settings import BASE_DIR
from dictionaries import models
from dictionaries.models import CHARACTERISTIC_CHOICES


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


def chapter_filter_by_filename(file):
    dictionary_id, chapter_num = re.search(r'(.*)-(.*)\..*', file).groups()
    logger.info('Dictionary ID is [%s], chapter number is [%s]', dictionary_id, chapter_num)
    return dictionary_id, chapter_num, models.Chapter.objects.filter(dictionary_id=dictionary_id,
                                                                     name__endswith=' %s' % chapter_num)


def insert_word(file: str, kana: str, kanji: str, characteristic: str, meaning: str) -> models.Word:
    if not kanji:
        kanji = ''

    if not kanji and not meaning:
        logger.warn('No meaning for %s' % kana)

    dictionary_id, chapter_num, chapter_filter = chapter_filter_by_filename(file)

    word_filter = models.Word.objects.filter(kana=kana, chapter=chapter_filter.get())

    # Words may have same kana and different kanji,
    # so check the meaning but not kanji when the kanji has '~' included
    word_filter = word_filter.filter(meaning=meaning)
    if word_filter.count() > 1:
        word_filter = word_filter.filter(kanji=kanji)

    marking = ''
    if '/' in kanji:
        kanji, marking = kanji.split('/')

    if word_filter.exists():
        word = word_filter.get()
        logger.info('Update kana=%s, kanji=%s, marking=%s, characteristic=%s, meaning=%s',
                    kana, kanji, marking, characteristic, meaning)
        word.kanji = kanji
        word.characteristic = characteristic
        word.marking = marking
        word.meaning = meaning
        word.save()
    else:
        # dictionary_id, chapter_num, chapter_filter = chapter_filter_by_filename(file)
        # logger.info('Dictionary ID is [%s], chapter number is [%s]', dictionary_id, chapter_num)
        logger.info('Insert kana=%s, kanji=%s, marking=%s, characteristic=%s, meaning=%s',
                    kana, kanji, marking, characteristic, meaning)

        # _filter = models.Chapter.objects.filter(dictionary_id=dictionary_id, name__endswith=' %s' % chapter_num)
        if chapter_filter.exists():
            chapter = chapter_filter.get()
            logger.info('Chapter [%s] already exists.', chapter)
            word = models.Word.objects.create(
                chapter=chapter, kana=kana, kanji=kanji, marking=marking,
                characteristic=characteristic, meaning=meaning)
            logger.info('Created!')
        else:
            raise RuntimeError('Chapter [%s-%s] not exist, init it first...' % (dictionary_id, chapter_num))
    return word


def init_chapters(dictionary_json):
    dictionary_json_id_ = dictionary_json['id']
    dictionary_json_name_ = dictionary_json['name']

    for chapter_json in dictionary_json['chapters']:
        chapter_json_name_ = chapter_json['name']
        if not models.Chapter.objects.filter(dictionary_id=dictionary_json_id_,
                                             name=chapter_json_name_).exists():
            logger.info('Create chapter %s to dictionary %s.', chapter_json_name_, dictionary_json_name_)
            models.Chapter.objects.create(dictionary_id=dictionary_json_id_, name=chapter_json_name_)


def init_dictionaries():
    with open(path.join(BASE_DIR, 'data/dictionaries.json')) as f:
        dictionaries_json = json.loads(f.read())
        logger.info('Init dictionaries: %s', dictionaries_json)

        for dictionary_json in dictionaries_json:
            dictionary_json_id_ = dictionary_json['id']
            dictionary_json_name_ = dictionary_json['name']
            logger.info('Init dictionary: %s', dictionary_json_name_)
            dictionary_filter = models.Dictionary.objects.filter(pk=dictionary_json_id_, name=dictionary_json_name_)
            if not dictionary_filter.exists():
                # logger.info('Dictionary [%s] already exists, setup chapters...', dictionary_json_name_)
                # else:
                logger.info('Dictionary [%s] not exist, create one...', dictionary_json_name_)
                models.Dictionary.objects.create(id=dictionary_json_id_, name=dictionary_json_name_)

            logger.info('Setup chapters...')
            init_chapters(dictionary_json)

        logger.info('Init dictionaries done.')


def clean_chapter(file, loaded_words):
    _, _, chapter_filter = chapter_filter_by_filename(file)
    for word_in_db in chapter_filter.get().words.values('id', 'kana', 'kanji', 'meaning').all():
        logger.info('word in db is %s', word_in_db)
        exists = len(list(filter(
            lambda word: word.kana == word_in_db['kana'] and
                         word.kanji == word_in_db['kanji'] and
                         word.meaning == word_in_db['meaning'],
            loaded_words))) > 0
        if not exists:
            logger.warn('remove %s - %s - %s - %s',
                        word_in_db['id'], word_in_db['kana'], word_in_db['kanji'], word_in_db['meaning'])
            models.Word.objects.get(pk=word_in_db['id']).delete()


def load_chapters(chapter_file: str = None):
    search_path = path.join(BASE_DIR, 'data/chapters')

    logger.info('Searching... %s', search_path)

    all_files = [f for f in listdir(search_path) if isfile(join(search_path, f))]
    logger.info('Files: %s', all_files)

    if chapter_file:
        all_files = [f for f in all_files if f == '%s.txt' % chapter_file]

    for file in all_files:
        logger.info('Try to load file: %s', file)
        loaded_words = []
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

                meaning = ''
                if len(parts) is 2:
                    characteristic = extract_characteristic()
                    meaning = parts[-1]
                elif len(parts) is 3:
                    characteristic = extract_characteristic(parts[1])
                    meaning = parts[-1]
                else:
                    logger.warn('~no such mode handler~ %s, skip...', parts)
                    # raise RuntimeError('format not recognised: %s' % parts)

                logger.info('characteristic is [%s]', characteristic)
                logger.info('meaning is [%s]', meaning)
                loaded_words.append(insert_word(file, kana, kanji, characteristic[0], meaning))
                logger.info('----------------------------------------------------')

        clean_chapter(file, loaded_words)


class Command(BaseCommand):
    help = "Load all chapters. Ignore exist words."

    def add_arguments(self, parser):
        parser.add_argument('--chapter', dest='chapter_file', help='load specified chapter file')

    def handle(self, *args, **options):
        init_dictionaries()
        load_chapters(options['chapter_file'])
