#!/usr/bin/env python
from setuptools import find_packages, setup
packages = find_packages()

VERSION = "0.1.1"
setup(name='mgpro',
      version=VERSION,
      author='Mijian Xu',
      author_email='gomijianxu@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      package_dir={'MGPro': 'mgpro'},
      install_requires=['pyproj', 'numpy', 'scipy', 'matplotlib'],
      entry_points={'console_scripts': ['mgpro=mgpro.client:main',
                                        'proj_convert=mgpro.proj:exec']},
      include_package_data=True,
      zip_safe=False
      )
