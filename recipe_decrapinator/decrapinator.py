import json
import os.path
import random
import re
import unicodedata
from contextlib import closing

import requests
from html.parser import HTMLParser
from io import StringIO
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.webdriver import Chrome



###### HELPERS

### HTML STRIPPER
## For cleaning scraped text
class html_stripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()
def strip_html_from_text(text_with_html):
    s = html_stripper()
    s.feed(str(text_with_html))
    return s.get_data()

### LI FIND SCHEMA SOUPER
## Ya
def perform_li_find(soup, schema, output_type):
    if schema['type'] == 'li-find':
        container = soup.find(class_=schema['container'])
        if container:
            servings_items = container.find_all(class_=schema['item'])
            for servings_item in servings_items:
                servings_text = strip_html_from_text(servings_item).lower()

                found = False
                lookfor_list = schema['lookfor']
                for lookfor in lookfor_list:
                    if lookfor.lower() in servings_text:
                        found = True
                if not found:
                    continue

                excludes = schema['exclude']
                for exclude in excludes:
                    servings_text = servings_text.replace(exclude.lower(), '').strip()

                if output_type == 'int':
                    try:
                        return int(servings_text)
                    except:
                        return 0
                elif output_type == 'text':
                    return str(servings_text)
                else:
                    return str(servings_text)
    return None



### STEP 1 INPUT URL
## Use decrapinate(url) > with recipe url
def decrapinate(url, schema=None, schemas=None):
    ## Get the validated url and hostname from the received url
    validated_url, hostname = validate_url(url)

    ## Check if a specific schema wants to be use
    if not schema:
        ## Get schema with hostname and additional schemas if provided
        schema = get_schema(hostname, schemas)

    ## Return processed recipe, created with the validated url and schema
    return process_recipe(validated_url, schema)

### STEP 2
##  Clean up this URL for schema search and web request
def validate_url(url):
    validated_url = None
    hostname = None
    if url:
        validated_url = 'https://' + url.replace('http://', '').replace('https://', '')
        if validated_url:
            parsed_url = urlparse(validated_url)
            if parsed_url and parsed_url.hostname:
                hostname = parsed_url.hostname
    return validated_url, hostname

### STEP 3
## Find the schema for this hostname
def get_schema(hostname, schemas=None):
    schema = None
    if hostname:
        ## If schemas are provided, use them first
        if schemas:
            try:
                schema = schemas[hostname]
            except:
                schema = None
        ## If we have not found a schema yet, use schemas/ directory
        if not schema:
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

### STEP 4
## Use URL and Schema to get soup (site data)
def process_recipe(url, schema, use_selenium=False):
    if not url or not schema:
        return {'error': 'invalid url'}
    output_data = []
    page_source = None
    if use_selenium:
        with closing(Chrome(executable_path="./chromedriver")) as browser:
            browser.get(url)
            page_source = browser.page_source
    else:
        web_data = requests.get(url)
        page_source = web_data.text
    soup = BeautifulSoup(page_source, 'lxml')
    if soup:
        basic_data = get_basic_info_from_soup(soup, schema)
        ingredient_data = get_ingredients_from_soup(soup, schema)
        direction_data = get_directions_from_soup(soup, schema, ingredient_data)
        output_data = [basic_data, ingredient_data, direction_data]
    return {'recipe_data': output_data}




### STEP 5
## Start building the data from soup
def get_basic_info_from_soup(soup, schema):
    output_data = {'hostname': schema['url'],
                   'image': get_image_from_soup(soup, schema),
                   'servings': get_servings_from_soup(soup, schema),
                   'yield': get_yield_from_soup(soup, schema),
                   'cook-time': get_cook_time_from_soup(soup, schema),
                   'prep-time': get_prep_time_from_soup(soup, schema),
                   'wait-time': get_wait_time_from_soup(soup, schema),
                   'total-time': get_total_time_from_soup(soup, schema)}
    return {'info': output_data}

### STEP 5.1
## Get recipe image from soup
def get_image_from_soup(soup, schema):
    image_schema = schema['basic'].get('image');
    if image_schema:
        schema_type = image_schema['type'];
        if schema_type == 'lazy':
            container = soup.find(class_=image_schema['container'])
            if container:
                item = container.find(class_=image_schema['item'])
                if item:
                    return item.get(image_schema['attr'])


### STEP 5.1
## Start building the data from soup
def get_servings_from_soup(soup, schema):
    servings = 0
    servings_schema = schema['basic'].get('servings')
    if servings_schema:
        schema_type = servings_schema['type']
        if schema_type == 'li-find':
            servings = perform_li_find(soup, servings_schema, 'int')
    return servings

### STEP 5.2
## Start building the data from soup
def get_yield_from_soup(soup, schema):
    yields = 0
    servings_schema = schema['basic'].get('yield')
    if servings_schema:
        schema_type = servings_schema['type']
        if schema_type == 'li-find':
            yields = perform_li_find(soup, servings_schema, 'text')
    return yields

### STEP 5.3
## Start building the data from soup
def get_prep_time_from_soup(soup, schema):
    prep_time = 0
    servings_schema = schema['basic'].get('prep-time')
    if servings_schema:
        schema_type = servings_schema['type']
        if schema_type == 'li-find':
            prep_time = perform_li_find(soup, servings_schema, 'time')
    return prep_time

### STEP 5.4
## Start building the data from soup
def get_total_time_from_soup(soup, schema):
    total_time = 0
    servings_schema = schema['basic'].get('total-time')
    if servings_schema:
        schema_type = servings_schema['type']
        if schema_type == 'li-find':
            total_time = perform_li_find(soup, servings_schema, 'time')
    return total_time

### STEP 5.5
## Start building the data from soup
def get_cook_time_from_soup(soup, schema):
    cook_time = 0
    servings_schema = schema['basic'].get('cook-time')
    if servings_schema:
        schema_type = servings_schema['type']
        if schema_type == 'li-find':
            cook_time = perform_li_find(soup, servings_schema, 'time')
    return cook_time

### STEP 5.6
## Start building the data from soup
def get_wait_time_from_soup(soup, schema):
    wait_time = 0
    servings_schema = schema['basic'].get('wait-time')
    if servings_schema:
        schema_type = servings_schema['type']
        if schema_type == 'li-find':
            wait_time = perform_li_find(soup, servings_schema, 'time')
    return wait_time




### STEP 6
## Gather the ingredients list from the soup
def get_ingredients_from_soup(soup, schema):
    output_data = {}
    ingredients_schema = schema['ingredients']
    schema_type = ingredients_schema['type']
    if schema_type == 'li':
        container = soup.find(class_=ingredients_schema['container'])
        if container:
            ingredients = container.find_all(class_=ingredients_schema['item'])

            step_count = 0
            for ingredient in ingredients:
                step_count += 1
                ingredient = ingredient.find(class_=ingredients_schema['text'])
                if ingredient:
                    ingredient = convert_ingredient(ingredient.text, step_count)
                    output_data = output_data | ingredient
    return {'ingredients': output_data }

### STEP 6.a
## Convert the ingredient text to dict object
def convert_ingredient(ingredient_text, step_count):
    ingredient_text = ingredient_text.lower()
    unit_of_measure, removed_uom = get_unit_of_measurement(ingredient_text)
    ingredient_required = '(optional)' not in ingredient_text
    amount = unicode_string_to_value(ingredient_text) or 0
    ingredient_name = get_ingredient_name(ingredient_text, removed_uom) or 'Unknown Ingredient'
    scale = 1
    return {ingredient_name: {
        'ingredient_id': step_count,
        'UOM': unit_of_measure,
        'amount': amount,
        'required': ingredient_required,
        'scaleFactor': scale,
        'original': ingredient_text.strip()
    }}

### STEP 6.a.1
## Get the unit of measurement from the ingredient text
def get_unit_of_measurement(ingredient_text):
    units = {
        'teaspoon': ['teaspoons', 'tsp', 'tsp.', 'teaspoon'],
        'dessertspoon': ['dessertspoons', 'dtsp', 'dtsp.', 'dessertspoon'],
        'tablespoon': ['tablespoons', 'tbsp', 'tbsp.', 'tablespoon'],
        'fluid ounce': ['fluid ounces', 'fl. oz.', 'fl oz', 'fluid ounce'],
        'cup': ['cups', 'cup'],
        'pint': ['pints', 'tsp', 'tsp.', 'pint'],
        'quart': ['quarts', 'qt', 'qt.','quart'],
        'lb': ['pounds', 'lb', 'lb.','pound'],
        'gallon': ['gallons', 'gal', 'gal.','gallon'],
        'pinch': ['pinches', 'pinch']
    }
    for key in units.keys():
        unit = units[key]
        for variant in unit:
            if variant in ingredient_text:
                return key, variant
    return None, ''

### STEP 6.a.2
## Convert unicode symbols to numeric values and add to the sum of other value in text.
def unicode_string_to_value(ingredient_text):
    filtered = ingredient_text.encode('ascii', 'ignore')
    values = [int(i) for i in filtered.decode().split() if i.isdigit()]
    value = sum(values)
    codes = re.sub(r"[\x00-\x7f]+", "", ingredient_text)
    for code in codes:
        try:
            value +=  unicodedata.numeric(u''.join(code))
        except:
            continue
    return value

### STEP 6.a.3
## Get a clean ingredient name from the ingredient text
def get_ingredient_name(ingredient_text, unit_of_measure):
    ingredient_text = ingredient_text.encode('ascii', 'ignore').decode()
    ingredient_text = ''.join([i for i in ingredient_text if not i.isdigit()])
    ingredient_text = ingredient_text.replace('(optional)', '')
    if unit_of_measure:
        ingredient_text = ingredient_text.replace(' ' + unit_of_measure, '')
    return ingredient_text.strip()




### STEP 7
## Gather the directions list from the soup
def get_directions_from_soup(soup, schema, ingredient_data):
    output_data = []
    directions_schema = schema['directions']
    schema_type = directions_schema['type']
    if schema_type == 'li':
        container = soup.find(class_=directions_schema['container'])
        if container:
            directions = container.find_all(class_=directions_schema['item'])
            step_count = 0
            for direction in directions:
                step_count += 1
                direction = direction.find(class_=directions_schema['text'])
                if direction:
                    output_data.append(convert_direction(direction, step_count, ingredient_data))

    return {'directions': output_data}

### STEP 7.a
## Convert the direction text to dict object
def convert_direction(direction_text, step_count, ingredient_data):
    direction = strip_html_from_text(direction_text)

    required  = True
    est_time = random.randrange(0, 59)

    ingredients = get_related_ingredients(direction, ingredient_data)


    return {'type': 'direction',
            'step': step_count,
            'original': direction,
            'required': required,
            'time': est_time,
            'ingredients_specified': ingredients,
    }

### STEP 7.a.1
## Get the related ingredients for each direction
def get_related_ingredients(direction, ingredient_datas):
    direction = direction.lower()
    ingredient_index = []
    ingredient_datas = ingredient_datas['ingredients']
    for key in ingredient_datas.keys():
        ingredient_data = ingredient_datas[key]
        ingredient_index.append([
            ingredient_data.get('ingredient_id'),
            key,
            ingredient_data.get('UOM'),
            ingredient_data.get('amount'),
            key.replace(',', '').replace('.', '').replace('!', '').split(' ')
        ])
    for ingredient in ingredient_index:
        for word in ingredient[4]:
            if len(word) > 2 and word in direction:
                ingredient_amount = unicode_string_to_value(direction)
                ingredient_amount_original = ingredient[3]
                diff = ingredient_amount_original - ingredient_amount
                if diff > 20 or diff < -20:
                    ingredient_amount = None
                return {ingredient[1]:{
                    'ingredient_id': ingredient[0],
                    'amount': ingredient_amount if not ingredient_amount or ingredient_amount == 0 else 'unspecified',
                    'UOM': ingredient[2]
                }}




### TESTING
if __name__ == '__main__':
    test = decrapinate('https://www.allrecipes.com/recipe/7284/irish-cream-chocolate-cheesecake/')
    test = json.dumps(test, sort_keys=True, indent=4)
    print(test)