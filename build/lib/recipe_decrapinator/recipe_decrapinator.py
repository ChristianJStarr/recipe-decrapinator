import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse




def decrapinate(url):
    return process_recipe(url, validate_url(url))

def validate_url(url):
    schema = None
    if url:
        parsed_url = urlparse(url)
        if parsed_url and parsed_url.hostname:
            try:
                f = open('schemas/' + parsed_url.hostname + '.json', 'r')
                data = f.read()
                f.close()
                if data:
                    schema = json.loads(data)
            except:
                return None
    return schema

def process_recipe(url, schema):
    if not url or not schema:
        return {'error': 'invalid url'}
    output_data = []
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    if soup:
        output_data = [get_basic_info_from_soup(soup, schema),
                       get_ingredients_from_soup(soup, schema),
                       get_directions_from_soup(soup, schema)]
    return {'recipe_data': output_data}

def get_basic_info_from_soup(soup, schema):
    output_data = {'hostname': schema['url'],
                   'servings': 0,
                   'yield': 0,
                   'cook-time': 0,
                   'prep-time': 0,
                   'wait_time': 0,
                   'total_time': 0}
    return {'info': output_data}

def get_ingredients_from_soup(soup, schema):
    output_data = []
    ingredients_schema = schema['ingredients']
    schema_type = ingredients_schema['type']

    return {'ingredients': output_data}

def get_directions_from_soup(soup, schema):
    output_data = []

    return {'directions': output_data}

