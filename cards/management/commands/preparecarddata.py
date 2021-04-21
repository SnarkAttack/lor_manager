from django.core.management.base import BaseCommand, CommandError
import os
import json
from cards.models import VocabTerm, Keyword, Region, SpellSpeed, Rarity, Set, Card

def get_static_abspath(p, route):
    return os.path.join(os.path.abspath('.'), 'cards/static/cards/lor_data', route, p)

def get_static_core_abspath(p):
    return get_static_abspath(p, 'core')

def get_static_set_abspath(p, set_name):
    return get_static_abspath(p, set_name)

def process_core_data(language_core_paths):

    card_id_dict = {
        'vocab_terms': {},
        'keywords': {},
        'regions': {},
        'spell_speeds': {},
        'rarities': {},
        'sets': {}
    }

    for language_core_path in language_core_paths:

        lor_lang_globals = None

        language = language_core_path.split('/')[-1]
        global_data_path = os.path.join(language_core_path, 'data', f"globals-{language}.json")
        with open(global_data_path, 'r') as f:
            lor_lang_globals = json.load(f)

        if lor_lang_globals is None:
            print(f"Error: could not find global data for {language}")

        try:
            vocab_terms = lor_lang_globals['vocabTerms']
            keywords = lor_lang_globals['keywords']
            regions = lor_lang_globals['regions']
            spell_speeds = lor_lang_globals['spellSpeeds']
            rarities = lor_lang_globals['rarities']
            sets = lor_lang_globals['sets']
        except KeyError as e:
            print(f"Missing {e} data for {language}")

        models_json = []

        for i, vocab_term in enumerate(vocab_terms):
            vocab_term_json = {
                "model": "cards.vocabterm",
                "pk": i+1,
                "fields": {
                    "name": vocab_term['name'],
                    "name_ref": vocab_term['nameRef'],
                    "description": vocab_term['description'],
                    "language": language
                }
            }

            card_id_dict['vocab_terms'][vocab_term['nameRef']] = i+1

            models_json.append(vocab_term_json)

        for i, keyword in enumerate(keywords):

            keyword_json = {
                "model": "cards.keyword",
                "pk": i+1,
                "fields": {
                    "name": keyword['name'],
                    "name_ref": keyword['nameRef'],
                    "description": keyword['description'],
                    "language": language
                }
            }

            card_id_dict['keywords'][keyword['nameRef']] = i+1

            models_json.append(keyword_json)

        for i, region in enumerate(regions):

            file_name = region['iconAbsolutePath'].split('/')[-1]

            region_json = {
                "model": "cards.region",
                "pk": i+1,
                "fields": {
                    "name": region['name'],
                    "name_ref": region['nameRef'],
                    "abbreviation": region['abbreviation'],
                    "file_name": file_name,
                    "language": language,
                }
            }

            card_id_dict['regions'][region['nameRef']] = i+1

            models_json.append(region_json)

        for i, spell_speed in enumerate(spell_speeds):

            spell_speed_json = {
                "model": "cards.spellspeed",
                "pk": i+1,
                "fields": {
                    "name": spell_speed['name'],
                    "name_ref": spell_speed['nameRef'],
                    "language": language,
                }
            }

            models_json.append(spell_speed_json)

            card_id_dict['spell_speeds'][spell_speed['nameRef']] = i+1

        for i, rarity in enumerate(rarities):

            rarity_json = {
                "model": "cards.rarity",
                "pk": i+1,
                "fields": {
                    "name": rarity['name'],
                    "name_ref": rarity['nameRef'],
                    "language": language,
                }
            }

            card_id_dict['rarities'][rarity['nameRef']] = i+1

            models_json.append(rarity_json)

        for set_data in sets:

            set_id = int(set_data['nameRef'][3:])

            set_json = {
                "model": "cards.set",
                "pk": set_id,
                "fields": {
                    "name": set_data['name'],
                    "name_ref": set_data['nameRef'],
                    "file_name": set_data['iconAbsolutePath'].split('/')[-1],
                    "language": language
                }
            }

            card_id_dict['sets'][set_data['nameRef']] = set_id

            models_json.append(set_json)

        with open(f'cards/fixtures/globals_{language}.json', 'w') as f:
            json.dump(models_json, f, indent=4)

        return card_id_dict

def get_all_sets():

    return [d for d in os.listdir('cards/static/cards/lor_data') if 'set' in d]

def process_card_data(language_set_paths, core_data_ids):

    for language in language_set_paths.keys():

        card_data = {}

        associated_cards = {}

        final_cards_json = []

        card_count = 0

        for s, lang_set_abspath in language_set_paths[language]:

            with open(f'cards/static/cards/lor_data/{s}/en_us/data/{s}-{language}.json', 'r') as f:
                card_json_data = json.load(f)

            for i, card in enumerate(card_json_data):

                card_json = {
                    "model": "cards.card",
                    "pk": card_count+i+1,
                    "fields": {
                        "asset_path": card['assets'][0]['gameAbsolutePath'].split('/')[-1],
                        "region": core_data_ids['regions'][card['regionRef']],
                        "attack": card['attack'],
                        "cost": card['cost'],
                        "health": card['health'],
                        "description": card['description'],
                        "description_raw": card['descriptionRaw'],
                        "level_up_description": card['levelupDescription'],
                        "level_up_description_raw": card['levelupDescriptionRaw'],
                        "flavor_text": card['flavorText'],
                        "artist_name": card['artistName'],
                        "name": card['name'],
                        "card_code": card['cardCode'],
                        "spell_speed": None if card['spellSpeed'] == "" else core_data_ids['spell_speeds'][card['spellSpeedRef']],
                        "rarity": core_data_ids['rarities'][card['rarityRef']],
                        "subtype": card['subtype'],
                        "supertype": card['supertype'],
                        "type": card['type'],
                        "collectible": card['collectible'],
                        "set": core_data_ids['sets'][card['set']],
                        "associated_cards": [],
                        "keywords": [core_data_ids['keywords'][keyword] for keyword in card['keywordRefs']]
                    }
                }

                card_data[card['cardCode']] = {
                    'card_json': card_json,
                    'card_id': i+1
                }

                associated_cards[card['cardCode']] = card['associatedCardRefs']

            card_count += i+1
            print(card_count)

        for card_code, card_info in card_data.items():
            associated_card_mappings = [card_data[assoc_code]['card_id'] for assoc_code in associated_cards[card_code]]
            card_json = card_info['card_json']
            card_json['associated_cards'] = associated_card_mappings
            final_cards_json.append(card_json)

        with open(f'cards/fixtures/cards_{language}.json', 'w') as f:
            json.dump(final_cards_json, f, indent=4)


class Command(BaseCommand):
    help = 'Prepares card data for loading into database'

    def add_arguments(self, parser):

        parser.add_argument(
            '--languages',
            help='List of languages to add to card database'
        )

    def handle(self, *args, **options):

        languages, language_core_paths = zip(*[(d, get_static_core_abspath(d)) for d in os.listdir('cards/static/cards/lor_data/core') if os.path.isdir(get_static_core_abspath(d))])

        if options['languages']:
            selected_languages = [lang.strip() for lang in options['languages'].split(',')]
            language_paths = [lang_path for lang, lang_path in zip(languages, language_core_paths) if lang in selected_languages]

        language_core_paths = [get_static_core_abspath(d) for d in os.listdir('cards/static/cards/lor_data/core') if os.path.isdir(get_static_core_abspath(d))]

        core_data_ids = process_core_data(language_core_paths)

        language_set_paths = {}

        for language in languages:
            language_set_paths[language] = [(s, get_static_set_abspath(language, s)) for s in get_all_sets()]

        process_card_data(language_set_paths, core_data_ids)
