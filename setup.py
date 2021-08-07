from distutils.core import setup
setup(
  name = 'package',         # How you named your package folder (MyLib)
  packages = ['yggdrasil'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Test package to upload to github',   # Give a short description about your library
  author = 'NeKo',                   # Type in your name
  url = 'https://github.com/JaPaNNeKo/utilities',   # Provide either the link to your github or to your website
  keywords = ['utilities', 'yggdrasil',],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'virtualenvwrapper-win',
      ],
)