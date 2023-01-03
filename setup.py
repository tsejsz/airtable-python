import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='airtable-python',
      version='0.1.0',
      description='API wrapper for Airtable written in Python',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      url='https://github.com/GearPlug/airtable-python',
      author='Juan Carlos Rios',
      author_email='juankrios15@gmail.com',
      license='MIT',
      packages=['airtable'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
