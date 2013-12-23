import multiprocessing
from setuptools import setup

setup(name='serf_master',
    version='0.1',
    description='helpers for writing manageable Serf handlers',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: System :: Systems Administration',
    ],
    keywords='serf',
    url='http://github.com/garethr/serf-master',
    author='Gareth Rushgrove',
    author_email='gareth@morethanseven.net',
    license='MIT',
    packages=['serf_master'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock',
    ],
    zip_safe=False)
