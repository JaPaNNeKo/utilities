from distutils.core import setup
setup(
  name='yggdrasil',
  packages=['yggdrasil'],
  version='1.1',
  license='MIT',
  description='Apps handler for in-house python scripts',
  author='mx',
  url='https://github.com/mx-personal/yggdrasil',
  keywords=['yggdrasil', 'app', 'virtual', 'environment'],
  install_requires=['virtualenvwrapper-win'],
  include_package_data=True,
  package_data={'': ['*.txt']},
)