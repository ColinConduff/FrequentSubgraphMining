from setuptools import setup

setup(name='gaston_py',
      version='0.1',
      description='Python implementation of the Gaston graph mining algorithm.',
      url='',
      author='Colin Conduff',
      author_email='colin.conduff@mst.edu',
      license='MIT',
      install_requires=[
          'networkx',
      ],
      scripts=['bin/gaston'],
      entry_points={
          'console_scripts': ['gaston=gaston_py.source.command_line:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
