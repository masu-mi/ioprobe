from setuptools import setup, find_packages
import os
import pypandoc

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = pypandoc.convert('README.md', 'rst')
except:
    README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'

install_requires = []


setup(name='ioprobe',
      version=version,
      description="Observation tool for I/O per process",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Environment :: Console',
        'Topic :: Utilities',
      ],
      keywords='proc system process io',
      author='Masumi Kanai',
      author_email='masumi.net@gmail.com',
      url='https://github.com/masu-mi/',
      license='The BSD 3-Clause License',
      packages=find_packages('src'),
      package_dir={'': 'src'}, include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['ioprobe=ioprobe:main']
      })
