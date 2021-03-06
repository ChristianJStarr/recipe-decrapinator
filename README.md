# recipe decrapinator

A simple package to scrape recipe information from major recipe sites.

## Hosted Demo
This package is being demonstrated at [recipe-decrapinator.info](https://www.recipe-decrapinator.info).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install recipe-decrapinator.


```bash
pip install recipe-decrapinator
```

## Usage

```python
from recipe_decrapinator.decrapinator import decrapinate

# returns recipe data object
recipe_data = decrapinate('www.somerecipes.com/chocolate-cake/')
```
## Recipe Data
```python
{'recipe_data': {
    'basic_info': {
        'hostname': 'www.somerecipes.com',
        'title': 'Chocolate Cake',
        'servings': 16,
    },
    'ingredients': {
        'large grade a egg': {
            'UOM': None,
            'amount': 2,
            'scaleFactor': 1,
            'required': True,
            'original': '2 large grade a eggs'
        },
        'white flour': {
            'UOM': 'cup',
            'amount': 1.333,
            'scaleFactor': 1,
            'required': True,
            'original': '1 \u2153 cup of white flour'
        }
    },
    'directions':{
        1:{
            'title': 'Put {0} into mixing bowl.',
            'vars':[
                {
                    'type': 'ingredient',
                    'name': 'Large Grade A Egg',
                    'amount': 'full'
                }
            ]  
        }
    }
}}
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/ChristianJStarr/recipe-decrapinator/blob/main/LICENSE)