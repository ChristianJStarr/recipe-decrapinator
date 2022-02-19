# recipe decrapinator

A simple package to scrape recipe information from major recipe sites.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install recipe-decrapinator
```

## Usage

```python
import recipe_decrapinator

# returns recipe data object
recipe_decrapinator.decrapinate('www.somerecipes.com/chocolate-cake/')
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
        'Large Grade A Egg': {
            'UOM': None,
            'amount': 2,
            'scaleFactor': 1
        },
        'White Flour': {
            'UOM': 'cup',
            'amount': 1.75,
            'scaleFactor': 1
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
[MIT](https://choosealicense.com/licenses/mit/)