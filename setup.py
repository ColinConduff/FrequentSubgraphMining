from setuptools import setup

setup(name='gaston_py',
      version='0.1',
      description='Python implementation of the Gaston graph mining algorithm.',
      url='',
      author='Colin Conduff',
      author_email='colin.conduff@mst.edu',
      license='MIT',
      packages=['gaston_py'],
      install_requires=[
          'networkx',
          'matplotlib'
      ],
      scripts=['bin/gaston'],
      entry_points={
          'console_scripts': ['gaston=gaston_py.gaston:gaston'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
