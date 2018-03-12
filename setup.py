from setuptools import find_packages, setup
packages=find_packages()

VERSION = "0.0.1"
setup(name='MGPro',
      version=VERSION,
      author='Mijian Xu',
      author_email='gomijianxu@gmail.com',
      packages=find_packages(),
      package_dir={'MGPro': 'mgpro'},
      install_requires=['numpy', 'scipy', 'matplotlib'],
      include_package_data=True,
      zip_safe=False
      )
