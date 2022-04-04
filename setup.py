from setuptools import setup, find_packages

setup(
  name='yggdrasil',
  packages=find_packages(),
  version='2.0-alpha',
  license='MIT',
  description='Apps handler for in-house python scripts',
  author='mx',
  url='https://github.com/mx-personal/yggdrasil',
  keywords=['yggdrasil', 'drivers', 'virtual', 'environment'],
  install_requires=[
    'pyyaml',
    'importlib_metadata',
  ],
  include_package_data=True,
  package_data={'yggdrasil': ['data/*.txt']},
)
