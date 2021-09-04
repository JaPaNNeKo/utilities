from distutils.core import setup
setup(
  name='yggdrasil',
  packages=['yggdrasil'],   # Chose the same as "name"
  version='1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='Apps handler for in-house python scripts',   # Give a short description about your library
  author='mx',                   # Type in your name
  url='https://github.com/mx-personal/yggdrasil',   # Provide either the link to your github or to your website
  keywords=['utilities', 'yggdrasil',],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'virtualenvwrapper-win',
      ],
  include_package_data=True,
  package_data={'': ['*.txt']},
)