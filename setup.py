from setuptools import setup

setup(
    name='bookmarks',
    packages=['bookmarks'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'SQLalchemy'
    ],
)
