from setuptools import setup, find_packages
import sys, os

version = '0.1'

def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)
    return open(path).read()

setup(name='toni',
      version=version,
      description="A ubercool (and just another) static website generator build on top of Flask, Frozen-Flask, Flask-FlatPages.",
      long_description=_read('README.md'),
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='',
      author='madflow',
      author_email='',
      url='https://github.com/madflow/toni',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'Flask',
        'Frozen-Flask',
        'Flask-FlatPages',
      ],
      entry_points={
          'console_scripts': [
              'toni = toni:main',
          ],
      }
      )
