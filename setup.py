from setuptools import setup
from setuptools import find_packages
from os.path import join, dirname
import retention

setup(
    name='abo_tools',
    version=retention.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)

install_requires=[
    'pandas==0.25.1',
    'numpy==1.16.5',
    'matplotlib==3.1.1',
    'plotly==4.4.1'
]