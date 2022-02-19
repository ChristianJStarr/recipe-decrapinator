import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse




def main():
    print('welcome to the recipe de-crapinator v1.0')

    url = prompt_for_recipe()
    schema = validate_url(url)

    while not schema:
        url = prompt_for_recipe(False)
        schema = validate_url(url)

    print('processing recipe url....')
    recipe_data = process_recipe(url, schema)
    print('saving recipe data....')
    save_recipe_data(recipe_data)

def validate_url(url):
    schema = None
    if url:
        parsed_url = urlparse(url)
        if parsed_url and parsed_url.hostname:
            try:
                f = open('schemas/' + parsed_url.hostname + '.json', 'r')
                print('file found')
                data = f.read()
                f.close()
                print(data)
                if data:
                    schema = json.loads(data)
            except:
                return None
    return schema

def prompt_for_recipe(supported=True):
    if not supported:
        print('this url is invalid or not supported yet.')
    return input('recipe url:')

def process_recipe(url, schema):
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
    if schema_type == 'li':
        
    return {'ingredients': output_data}

def get_directions_from_soup(soup, schema):
    output_data = []

    return {'directions': output_data}

def save_recipe_data(recipe_data):
    file_name = 'recipe_output.json'
    if not recipe_data:
        print('invalid recipe data')
        return False

    try:
        recipe_json_data = json.dumps(recipe_data)
        f = open(file_name, 'w')
        f.write(recipe_json_data)
        f.close()
        print("saving successful. \nOUTPUT: '", file_name, "'")
        return True
    except:
        print("saving failed. \nRECIPE DATA: \n", recipe_data)
        return False

if __name__ == "__main__":
    main()