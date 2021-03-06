from setuptools import setup

setup(
    name='recipe-decrapinator',
    version='0.0.7',
    description='A simple package to scrape recipe information.',
    url='https://github.com/christianjstarr/recipe-decrapinator',
    author='Christian Starr',
    author_email='christianjstarr@icloud.com',
    license='MIT',
    packages=['recipe_decrapinator'],
    package_data = {
        '': ['schemas/*.json'],
    },
    install_requires=['bs4',
                      'requests',
                      'selenium'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
