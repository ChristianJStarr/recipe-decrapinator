import json
import os.path
import re
import unicodedata

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse




def decrapinate(url):
    validated_url, hostname = validate_url(url)
    return process_recipe(validated_url, get_schema(hostname))

def validate_url(url):
    validated_url = None
    hostname = None
    if url:
        validated_url = url.replace('https://', '')
        validated_url = validated_url.replace('http://', '')
        validated_url = 'https://' + validated_url
        if validated_url:
            parsed_url = urlparse(validated_url)
            if parsed_url and parsed_url.hostname:
                hostname = parsed_url.hostname
    return validated_url, hostname

def get_schema(hostname):
    schema = None
    if hostname:
        local_path = 'schemas/' + hostname + '.json'
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), local_path)
        if os.path.isfile(full_path):
            try:
                f = open(full_path, 'r')
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
    output_data = {}
    ingredients_schema = schema['ingredients']
    schema_type = ingredients_schema['type']
    if schema_type == 'li':
        container = soup.find(class_=ingredients_schema['container'])
        if container:
            ingredients = container.find_all(class_=ingredients_schema['item'])
            for ingredient in ingredients:
                ingredient = ingredient.find(class_=ingredients_schema['text'])
                if ingredient:
                    ingredient = convert_ingredient(ingredient.text)
                    output_data = output_data | ingredient
    return {'ingredients': output_data }

def convert_ingredient(ingredient_text):
    ingredient_text = ingredient_text.lower()
    unit_of_measure = get_unit_of_measurement(ingredient_text)
    amount = unicode_string_to_value(ingredient_text) or 0
    ingredient_name = get_ingredient_name(ingredient_text, unit_of_measure) or 'Unknown Ingredient'
    scale = 1
    return {ingredient_name: {
        'UOM': unit_of_measure,
        'amount': amount,
        'scaleFactor': scale,
        'original': ingredient_text.strip()
    }}

def get_directions_from_soup(soup, schema):
    output_data = []

    return {'directions': output_data}

def get_ingredient_name(ingredient_text, unit_of_measure):
    ingredient_text = ingredient_text.encode('ascii', 'ignore').decode()
    ingredient_text = ''.join([i for i in ingredient_text if not i.isdigit()])
    if unit_of_measure:
        ingredient_text = ingredient_text.replace(unit_of_measure + ' ', '')
    return ingredient_text.strip()

def get_unit_of_measurement(ingredient_text):
    units = ['teaspoon', 'dessertspoon', 'tablespoon', 'fluid ounce',
             'cup', 'pint', 'quart', 'gallon']
    for unit in units:
        if unit in ingredient_text:
            return unit


def unicode_string_to_value(ingredient_text):
    filtered = ingredient_text.encode('ascii', 'ignore')
    values = [int(i) for i in filtered.decode().split() if i.isdigit()]
    value = sum(values)
    codes = re.sub(r"[\x00-\x7f]+", "", ingredient_text)
    for code in codes:
        value +=  unicodedata.numeric(u''.join(code))
    return value



if __name__ == '__main__':
    test = decrapinate('https://www.allrecipes.com/recipe/54165/balsamic-bruschetta/')
    test = json.dumps(test, sort_keys=True, indent=4)
    print(test)

