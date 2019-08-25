from distutils.core import setup

setup(
    name='tfl-tree',
    version='0.0.1',
    packages=['tfltree', 'tfltree.raspberrypi'],
    install_requires=[
        'pymediainfo==4.0',
        'requests==2.22.0'
    ],
)
