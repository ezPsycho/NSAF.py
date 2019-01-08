from setuptools import setup, find_packages

setup(
    name = 'NSAF',
    version = '0.0.3',
    keywords='nsaf neuroscience atlas brain',
    description = 'A python lib non-standard atlas format',
    license = 'MIT License',
    url = 'https://github.com/ezPsycho/NSAF.py',
    author = 'Losses',
    author_email = 'losses@m-b.science',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)