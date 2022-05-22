from setuptools import setup, find_packages

setup(
  name='yggdrasil',
  packages=find_packages(),
  version='2.0.0-alpha.7',
  description='Apps handler for in-house python scripts',
  author='Umbriel Draken',
  long_description='README',
  long_description_content_type='text/markdown',
  author_email='umbriel.draken@gmail.com',
  url='https://github.com/um-en/yggdrasil',
  license='MIT',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows :: Windows 10',
  ],
  keywords=['yggdrasil', 'drivers', 'virtual', 'environment'],
  install_requires=[
    'pyyaml',
    'dist_meta@git+https://github.com/um-en/dist_meta.git@1.0.0'
  ],
  entry_points={
    'console_scripts': ['yggdrasil=yggdrasil.scripts:cmd_ygg']
  },
  include_package_data=True,
  package_data={'yggdrasil': ['data/*.txt', 'data/*.yaml']},
)
